def mapear_status(eventos):

    if not eventos:
        return None

    ultimo = eventos[-1]

    descricao = ultimo.get("descricao", "").lower()

    if "coleta" in descricao:
        return "pedido coletado"

    if "transferencia" in descricao:
        return "em transporte"

    if "rota de entrega" in descricao:
        return "saiu para entrega"

    if "entrega realizada" in descricao or "comprovante" in descricao:
        return "entrega concluida"

    return "em transporte"