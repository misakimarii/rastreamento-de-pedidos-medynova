from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import os

from app.jobs.importar_pedidos import importar_pedidos
from app.dependencies.auth import require_admin

router = APIRouter(tags=["Upload"])

PASTA_PLANILHAS = "planilhas"
NOME_ARQUIVO = "Planilha_Notas.CSV"


@router.post("/upload-planilha")
async def upload_planilha(
    file: UploadFile = File(...),
    user=Depends(require_admin)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Nenhum arquivo enviado")

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Envie um arquivo CSV")

    try:
        os.makedirs(PASTA_PLANILHAS, exist_ok=True)

        for nome_arquivo in os.listdir(PASTA_PLANILHAS):
            if nome_arquivo.lower().endswith(".csv"):
                os.remove(os.path.join(PASTA_PLANILHAS, nome_arquivo))

        caminho_arquivo = os.path.join(PASTA_PLANILHAS, NOME_ARQUIVO)

        with open(caminho_arquivo, "wb") as buffer:
            buffer.write(await file.read())

        importar_pedidos()

        return {
            "success": True,
            "mensagem": "Planilha enviada, substituída e importada com sucesso"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar planilha: {str(e)}")