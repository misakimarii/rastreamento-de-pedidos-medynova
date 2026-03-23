from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler

from app.database import engine, SessionLocal
from app.models import Base
from app.models.pedido import Pedido

from app.jobs.atualizar_entregas import atualizar_entregas
from app.jobs.importar_pedidos import importar_pedidos

from app.routers.rastreamento import router as rastreamento_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(rastreamento_router)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/pedido/{numero_nf}")
def buscar_pedido(numero_nf: str, db: Session = Depends(get_db)):

    numero_nf = numero_nf.lstrip("0")

    pedido = db.query(Pedido).filter_by(numero_nf=numero_nf).first()

    if not pedido:
        return {"erro": "Pedido não encontrado"}

    return {
        "numero_nf": pedido.numero_nf,
        "chave_nfe": pedido.chave_nfe,
        "cidade": pedido.cidade
    }


scheduler = BackgroundScheduler()

scheduler.add_job(importar_pedidos, "interval", minutes=5, max_instances=1)
scheduler.add_job(atualizar_entregas, "interval", minutes=15, max_instances=1)

scheduler.start()