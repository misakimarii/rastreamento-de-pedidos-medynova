from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi.middleware.cors import CORSMiddleware

import threading

from app.database import engine, SessionLocal
from app.models import Base
from app.models.pedido import Pedido

from app.jobs.atualizar_entregas import atualizar_entregas
from app.jobs.importar_pedidos import importar_pedidos

from app.routers.rastreamento import router as rastreamento_router
from app.routers.upload_planilha import router as upload_planilha_router
from app.routers.admin_auth import router as admin_auth_router

app = FastAPI()
scheduler = BackgroundScheduler()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rastreamento_router)
app.include_router(upload_planilha_router)
app.include_router(admin_auth_router)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def startup_event():
    print("🚀 Iniciando sistema...")

    threading.Thread(target=importar_pedidos).start()
    threading.Thread(target=atualizar_entregas).start()

    print("⏰ Iniciando scheduler...")

    if not scheduler.running:
        scheduler.add_job(importar_pedidos, "interval", minutes=5, max_instances=1)
        scheduler.add_job(atualizar_entregas, "interval", minutes=15, max_instances=1)
        scheduler.start()


@app.on_event("shutdown")
def shutdown_event():
    print("🛑 Encerrando scheduler...")
    if scheduler.running:
        scheduler.shutdown()


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