from app.database import SessionLocal
from app.models.pedido import Pedido


def normalizar(valor):
    if not valor:
        return ""
    return str(valor).strip().lstrip("0")


def salvar_pedidos(df):
    db = SessionLocal()

    novos = 0

    for _, row in df.iterrows():

        numero_nf = normalizar(row.get("Numero"))
        chave = normalizar(row.get("Chave NF-e"))

        if not numero_nf or not chave:
            continue

        existe = db.query(Pedido).filter(
            Pedido.numero_nf == numero_nf
        ).first()

        if existe:
            continue

        try:
            pedido = Pedido(
                numero_nf=numero_nf,
                chave_nfe=chave,
                cidade=(row.get("Cliente/Fornecedor") or "").strip(),
                uf=(row.get("UF") or "").strip()
            )

            db.add(pedido)
            db.commit()
            novos += 1

        except Exception as e:
            db.rollback()
            print("Erro ao salvar:", e)
            continue

    db.close()

    print(f" {novos} novos pedidos salvos!")