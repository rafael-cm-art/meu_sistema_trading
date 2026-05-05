import requests
import pandas as pd

API_KEY = "SUA_API_KEY_AQUI"

def pegar_dados(ativo):
    try:
        url = f"https://api.twelvedata.com/time_series?symbol={ativo}&interval=1min&outputsize=50&apikey={API_KEY}"

        response = requests.get(url)
        data = response.json()

        if "values" not in data:
            return None, 0, 0, "SEM DADOS"

        df = pd.DataFrame(data["values"])

        # converter tipos
        df["datetime"] = pd.to_datetime(df["datetime"])
        df = df.sort_values("datetime")

        for col in ["open", "high", "low", "close"]:
            df[col] = df[col].astype(float)

        df.rename(columns={
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close"
        }, inplace=True)

        # suporte e resistência simples
        suporte = df["Low"].min()
        resistencia = df["High"].max()

        # sinal básico
        ultimo = df["Close"].iloc[-1]
        media = df["Close"].mean()

        sinal = "COMPRA" if ultimo > media else "VENDA"

        return df, suporte, resistencia, sinal

    except Exception as e:
        print("Erro API:", e)
        return None, 0, 0, "ERRO"