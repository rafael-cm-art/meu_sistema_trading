import yfinance as yf

def pegar_dados(ativo):
    df = yf.download(ativo, period="5d", interval="15m")

    if df is None or df.empty:
        return df, 0.0, 0.0, "Sem dados"

    # 🔥 GARANTE DATA LIMPA (remove lixo do yfinance)
    df = df.dropna()

    # =========================
    # 📊 SUPORTE / RESISTÊNCIA
    # =========================
    suporte = float(df["Low"].to_numpy().min())
    resistencia = float(df["High"].to_numpy().max())

    # =========================
    # 🎯 SINAL SIMPLES
    # =========================
    closes = df["Close"].tail(5).to_numpy()

    if len(closes) < 5:
        sinal = "Sem dados"
    elif all(closes[i] > closes[i-1] for i in range(1, 5)):
        sinal = "📈 COMPRA"
    elif all(closes[i] < closes[i-1] for i in range(1, 5)):
        sinal = "📉 VENDA"
    else:
        sinal = "⏸️ NEUTRO"

    return df, suporte, resistencia, sinal
=======
    return df, suporte, resistencia, sinal

