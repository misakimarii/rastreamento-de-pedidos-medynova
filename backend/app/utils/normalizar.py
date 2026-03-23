def normalizar_chave(chave):
    if not chave:
        return None

    return str(chave).lstrip("0")