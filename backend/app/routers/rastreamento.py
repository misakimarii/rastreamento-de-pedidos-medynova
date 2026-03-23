from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.pedido import Pedido
from app.models.evento_entrega import EventoEntrega
from app.utils.cache import get_cache, set_cache

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/rastreamento/{numero_nf}")
def rastrear(numero_nf: str, db: Session = Depends(get_db)):

    numero_nf = numero_nf.lstrip("0")

    cache = get_cache(numero_nf)
    if cache:
        return cache

    pedido = db.query(Pedido).filter(
        Pedido.numero_nf == numero_nf
    ).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Nota fiscal não encontrada")

    eventos = db.query(EventoEntrega).filter(
        EventoEntrega.pedido_id == pedido.id
    ).order_by(EventoEntrega.data_evento).all()

    if not eventos:
        raise HTTPException(status_code=404, detail="Nenhum evento encontrado")

    lista_eventos = []

    for evento in eventos:
        lista_eventos.append({
            "status": evento.status,
            "data": evento.data_evento.strftime("%d/%m/%Y"),
            "hora": evento.data_evento.strftime("%H:%M:%S")
        })

    resposta = {
        "nf": numero_nf,
        "cidade": pedido.cidade,
        "eventos": lista_eventos
    }

    set_cache(numero_nf, resposta)

    return resposta