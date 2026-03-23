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

        token = data.get("data", {}).get("access_key")

        _token_cache["token"] = token
        _token_cache["expira_em"] = datetime.now() + timedelta(minutes=30)

        return token

    except Exception as e:
        logger.error(f"Erro login API: {e}")
        return None


def consultar_nfe(chave):

    token = obter_token()

    if not token:
        return None

    url = f"{BASE_URL}/api/v1/tracking/ocorrencias/nfe"

    params = {
        "chave": chave,
        "comprovante": 0
    }

    headers = {
        "Authorization": f"Bearer {token}"
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

        eventos = data["data"][0]["dados"]

        return eventos

    except requests.exceptions.Timeout:

        logger.error("Timeout na API da transportadora")
        return None

    except Exception as e:

        logger.error(f"Erro inesperado: {e}")
        return None