import pandas as pd


def importar_planilha(caminho):
    try:
        print(f"📄 Lendo arquivo: {caminho}")

        df = pd.read_csv(
            caminho,
            sep=";",
            encoding="latin-1",
            skiprows=2,
            dtype=str  
        )

        df = df.dropna(how="all")

        df = df.fillna("")

        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

        df = df[df["Numero"] != ""]

        df = df[~df["Numero"].str.contains("TOTAL", na=False)]

        print(f"{len(df)} registros carregados")

        return df

    except Exception as e:
        print(f"Erro ao ler CSV: {e}")
        return None