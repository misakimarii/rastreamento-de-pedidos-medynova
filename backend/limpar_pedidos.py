from app.database import SessionLocal
from app.models.pedido import Pedido

db = SessionLocal()

db.query(Pedido).delete()
db.commit()

db.close()

print("✅ Todos os pedidos apagados!")