def normalizar_numero_nf(valor):
    if not valor:
        return ""

    valor = str(valor).strip()

    if valor.endswith(".0"):
        valor = valor[:-2]

    valor = "".join(filter(str.isdigit, valor))

    valor = valor.lstrip("0")

    return valor


def normalizar_chave(chave):
    if not chave:
        return ""

    chave = str(chave).strip()

    chave = "".join(filter(str.isdigit, chave))

    return chave