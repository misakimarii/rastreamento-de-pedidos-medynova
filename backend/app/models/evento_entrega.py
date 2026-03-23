from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class EventoEntrega(Base):

    __tablename__ = "eventos_entrega"

    id = Column(Integer, primary_key=True, index=True)

    pedido_id = Column(Integer, ForeignKey("pedidos.id"))

    status = Column(String)
    descricao = Column(String)
    data_evento = Column(DateTime)

    pedido = relationship("Pedido")