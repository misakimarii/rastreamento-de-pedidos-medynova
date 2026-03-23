import schedule
import time

from app.services.importar_planilha import importar_planilha
from app.services.salvar_pedidos import salvar_pedidos


def job():
    print("Rodando importação automática...")

    df = importar_planilha("planilhas/Pedidos.CSV")
    salvar_pedidos(df)

    print("Finalizado!")


schedule.every().day.at("08:00").do(job)

job()

while True:
    schedule.run_pending()
    time.sleep(60)