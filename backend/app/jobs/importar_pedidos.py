import os
from app.services.importar_planilha import importar_planilha
from app.services.salvar_pedidos import salvar_pedidos

PASTA = "planilhas"


def importar_pedidos():

    print(" Verificando planilhas...")

    arquivos = os.listdir(PASTA)

    for arquivo in arquivos:

        if not arquivo.endswith(".csv"):
            continue

        caminho = os.path.join(PASTA, arquivo)

        print(f" Importando: {arquivo}")

        df = importar_planilha(caminho)
        salvar_pedidos(df)

        pasta_processados = os.path.join(PASTA, "processados")

        if not os.path.exists(pasta_processados):
            os.makedirs(pasta_processados)

        novo_caminho = os.path.join(pasta_processados, arquivo)

        os.rename(caminho, novo_caminho)

        print(f" {arquivo} movido para processados")