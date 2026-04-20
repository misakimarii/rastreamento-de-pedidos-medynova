import os
from app.services.importar_planilha import importar_planilha
from app.services.salvar_pedidos import salvar_pedidos


def importar_pedidos():
    print("🔍 Procurando arquivos CSV...")

    pasta = "planilhas"

    if not os.path.exists(pasta):
        print(" Pasta de planilhas não encontrada")
        return

    arquivos = os.listdir(pasta)

    csvs = [f for f in arquivos if f.lower().endswith(".csv")]

    if not csvs:
        print(" Nenhum CSV encontrado")
        return

    for arquivo in csvs:
        caminho = os.path.join(pasta, arquivo)

        print(f" Importando: {arquivo}")

        try:
            df = importar_planilha(caminho)

            if df is None:
                continue

            salvar_pedidos(df)

        except Exception as e:
            print(f" Erro ao importar {arquivo}: {e}")