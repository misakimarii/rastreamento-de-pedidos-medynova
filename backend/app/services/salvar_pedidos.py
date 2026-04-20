from app.database import SessionLocal
from app.models.pedido import Pedido
from app.utils.normalizador import normalizar_numero_nf


def salvar_pedidos(df):
    if df is None:
        print("DataFrame vazio")
        return

    db = SessionLocal()
    novos = 0

    for _, row in df.iterrows():

        chave = str(row.get("Chave NF-e", "")).strip()

        if not chave:
            continue

        numero_nf = normalizar_numero_nf(row.get("Numero", ""))

        if not numero_nf:
            continue

        existe = db.query(Pedido).filter(
            Pedido.numero_nf == numero_nf
        ).first()

        if existe:
            print(f"Pedido {numero_nf} já existe, ignorando...")
            continue

        try:
            pedido = Pedido(
                numero_nf=numero_nf,
                chave_nfe=chave,
                cidade=str(row.get("Cliente/Fornecedor", "")),
                uf=str(row.get("UF", ""))
            )

            db.add(pedido)
            db.commit()
            novos += 1

        except Exception as e:
            print(f"Erro ao salvar pedido {numero_nf}: {e}")
            db.rollback()

    db.close()

    print(f"{novos} novos pedidos salvos!")