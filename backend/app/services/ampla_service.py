import requests
from app.config import AMPLA_USER, AMPLA_SENHA, BASE_URL
from app.logger import logger
from datetime import datetime, timedelta

_token_cache = {
    "token": None,
    "expira_em": None
}


def obter_token():
    if _token_cache["token"] and _token_cache["expira_em"]:
        if datetime.now() < _token_cache["expira_em"]:
            return _token_cache["token"]

    url = f"{BASE_URL}/api/v1/acesso/auth/login"

    payload = {
        "usuario": AMPLA_USER,
        "senha": AMPLA_SENHA
    }

    try:
        response = requests.post(url, json=payload, timeout=10)

        if response.status_code != 200:
            logger.error(f"Erro ao gerar token: {response.status_code}")
            return None

        data = response.json()
        print("RESPOSTA LOGIN:", data)

        token = data.get("data", {}).get("access_key")
        if not token:
            logger.error("Token não encontrado na resposta de login.")
            return None

        _token_cache["token"] = token
        _token_cache["expira_em"] = datetime.now() + timedelta(minutes=30)

        return token

    except Exception as e:
        logger.error(f"Erro login API: {e}")
        return None


def parse_data_evento(data_str, hora_str=None):
    try:
        if not data_str:
            return None

        if " " in data_str and "-" in data_str:
            return datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")


        if hora_str:
            return datetime.strptime(f"{data_str} {hora_str}", "%d/%m/%Y %H:%M:%S")

        return datetime.strptime(data_str, "%d/%m/%Y")

    except Exception as e:
        print("ERRO AO PARSEAR DATA:", data_str, hora_str, e)
        return None


def formatar_previsao(data_str):
    if not data_str:
        return None

    formatos = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d/%m/%Y %H:%M:%S"
    ]

    for formato in formatos:
        try:
            dt = datetime.strptime(data_str, formato)
            return dt.strftime("%d/%m")
        except:
            continue

    return None


def consultar_nfe(chave_nfe, numero_nf):
    token = obter_token()

    if not token:
        return None

    # CORRETO: endpoint de tracking com /api/v1
    url = f"{BASE_URL}/api/v1/tracking/ocorrencias/nfe"

    params = {
        "chave": chave_nfe,
        "comprovante": 0
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json"
    }


    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10
        )

        if response.status_code != 200:
            logger.error(f"Erro API transportadora: {response.status_code}")
            return None

        data = response.json()
        dados = data.get("data", [])

        if not dados:
            return None

        eventos_tratados = []

        for item in dados:
            for evento in item.get("dados", []):
                data_evento = evento.get("data")
                hora_evento = evento.get("hora")

                dt = parse_data_evento(data_evento, hora_evento)

                if not dt:
                    continue

                eventos_tratados.append({
                    "status": evento.get("descricao") or evento.get("status"),
                    "data": data_evento,
                    "hora": hora_evento or evento.get("hora_entrega") or "",
                    "datetime": dt
                })

        if not eventos_tratados:
            print("❌ NENHUM EVENTO ENCONTRADO")
            return None

        eventos_tratados.sort(key=lambda x: x["datetime"], reverse=True)

        eventos_final = [
            {
                "status": e["status"],
                "data": e["data"],
                "hora": e["hora"]
            }
            for e in eventos_tratados
        ]

        primeiro_item = dados[0]

        previsao_bruta = (
            primeiro_item.get("prev_entrega")
            or primeiro_item.get("data_entrega")
            or primeiro_item.get("entrega", {}).get("data_entrega")
        )

        previsao_formatada = formatar_previsao(previsao_bruta)

        return {
            "eventos": eventos_final,
            "previsao_entrega": previsao_formatada
        }

    except requests.exceptions.Timeout:
        logger.error("Timeout na API da transportadora")
        return None

    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        return None