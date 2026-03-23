from app.database import SessionLocal
from app.models.pedido import Pedido
from app.models.evento_entrega import EventoEntrega
from app.services.ampla_service import consultar_nfe
from app.utils.normalizar import normalizar_chave
from datetime import datetime


def atualizar_entregas():

    db = SessionLocal()

    pedidos = db.query(Pedido).all()

    for pedido in pedidos:

        chave = normalizar_chave(pedido.chave_nfe)

        eventos = consultar_nfe(chave)

        if not eventos:
            continue

        for evento in eventos:

            descricao = evento.get("descricao")
            data_evento = evento.get("data")

            existe = db.query(EventoEntrega).filter(
                EventoEntrega.pedido_id == pedido.id,
                EventoEntrega.descricao == descricao
            ).first()

            if existe:
                continue

            novo_evento = EventoEntrega(
                pedido_id=pedido.id,
                status=descricao,
                descricao=descricao,
                data_evento=datetime.fromisoformat(data_evento)
            )

            db.add(novo_evento)

    db.commit()
    db.close()