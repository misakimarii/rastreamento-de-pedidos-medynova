from sqlalchemy import Column, Integer, String
from app.database import Base

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    numero_nf = Column(String)
    chave_nfe = Column(String, unique=True, index=True) 
    cidade = Column(String)
    uf = Column(String)