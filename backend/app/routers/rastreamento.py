from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.pedido import Pedido
from app.utils.cache import get_cache, set_cache
from app.utils.normalizador import normalizar_numero_nf
from app.services.ampla_service import consultar_nfe
from app.utils.prazo_entrega import calcular_previsao

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/rastreamento/{numero_nf}")
def rastrear(numero_nf: str, db: Session = Depends(get_db)):


    numero_nf = normalizar_numero_nf(numero_nf)

    cache = get_cache(numero_nf)
    if cache:
        return cache

    pedido = db.query(Pedido).filter(
        Pedido.numero_nf == numero_nf
    ).first()

    if not pedido:
        print("❌ PEDIDO NÃO ENCONTRADO NO BANCO")
        raise HTTPException(status_code=404, detail="Nota fiscal não encontrada")

    print("✅ PEDIDO ENCONTRADO")

    print("CHAVE DO BANCO:", pedido.chave_nfe)

    resultado_api = consultar_nfe(pedido.chave_nfe, numero_nf)

    if not resultado_api:
        return {
        "success": True,
        "nf": numero_nf,
        "cidade": pedido.cidade,
        "eventos": [],
        "previsao_entrega": None,
        "status": "Pedido em processamento na transportadora"
    }

    lista_eventos = resultado_api.get("eventos", [])

    if not lista_eventos:
        raise HTTPException(status_code=404, detail="Nenhum evento encontrado")

    previsao = resultado_api.get("previsao_entrega")

    if not previsao:
        previsao = calcular_previsao(pedido, lista_eventos)

    print("EVENTOS FINAIS:", lista_eventos)
    print("PREVISAO FINAL:", previsao)

    resposta = {
        "success": True,
        "nf": numero_nf,
        "cidade": pedido.cidade,
        "eventos": lista_eventos,
        "previsao_entrega": previsao
    }

    set_cache(numero_nf, resposta)

    return resposta