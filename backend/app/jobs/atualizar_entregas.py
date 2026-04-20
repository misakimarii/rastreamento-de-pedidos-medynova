from app.database import SessionLocal
from app.models.pedido import Pedido
from app.models.evento_entrega import EventoEntrega
from app.services.ampla_service import consultar_nfe
from datetime import datetime


def atualizar_entregas():
    db = SessionLocal()

    pedidos = db.query(Pedido).all()

    for pedido in pedidos:

        resultado = consultar_nfe(pedido.chave_nfe, pedido.numero_nf)
        if not resultado:
            continue

        eventos = resultado.get("eventos", [])

        for evento in eventos:

            descricao = evento.get("descricao")
            data_evento = evento.get("data")

            if not descricao or not data_evento:
                continue

            try:
                data_formatada = datetime.fromisoformat(data_evento)
            except Exception:
                continue

            existe = db.query(EventoEntrega).filter(
                EventoEntrega.pedido_id == pedido.id,
                EventoEntrega.descricao == descricao,
                EventoEntrega.data_evento == data_formatada
            ).first()

            if existe:
                continue

            novo_evento = EventoEntrega(
                pedido_id=pedido.id,
                status=descricao,
                descricao=descricao,
                data_evento=data_formatada
            )

            db.add(novo_evento)

    db.commit()
    db.close()

    print("Eventos atualizados!")