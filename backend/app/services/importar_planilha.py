import pandas as pd

def importar_planilha(caminho):
    with open(caminho, "r", encoding="cp1252") as f:
        linhas = f.readlines()

    inicio = 0
    for i, linha in enumerate(linhas):
        if "Cli_For" in linha:
            inicio = i
            break

    df = pd.read_csv(
        caminho,
        sep=";",
        dtype=str,
        encoding="cp1252",
        skiprows=inicio,
        engine="python",
        on_bad_lines="skip"
    )

    df.columns = df.columns.str.encode('latin1').str.decode('utf-8')
    df.columns = df.columns.str.replace("C�digo", "Codigo")

    df = df[df["Numero"].str.isnumeric()]
    df = df.reset_index(drop=True)
    df = df.fillna("")

    print(f"✅ {len(df)} registros carregados")

    return df