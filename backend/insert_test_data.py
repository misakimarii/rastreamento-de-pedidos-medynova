from app.database import SessionLocal
from app.models.pedido import Pedido

db = SessionLocal()

pedido = Pedido(
    numero_nf="1028",
    chave_nfe="26260229094796000170550010000010281554176745",
    cidade= "Recife",
    uf= "PE"
)

db.add(pedido)
db.commit()

print("Pedido inserido com sucesso!")