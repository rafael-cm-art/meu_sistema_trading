from flask import Flask, render_template
from flask_socketio import SocketIO
from dados import pegar_dados
import threading

app = Flask(__name__)

# ✔ CONFIGURAÇÃO CORRETA PARA RENDER
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet"
)

ativo_global = "PETR4.SA"

# ---------------------------
# PÁGINA
# ---------------------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------------------
# FUNÇÃO SEGURA PARA FLOAT
# ---------------------------
def to_float(valor):
    try:
        if hasattr(valor, "iloc"):
            return float(valor.iloc[0])
        return float(valor)
    except:
        return 0.0

# ---------------------------
# THREAD DE ATUALIZAÇÃO
# ---------------------------
def atualizar_dados():
    global ativo_global

    while True:
        try:
            df, suporte, resistencia, sinal = pegar_dados(ativo_global)

            if df is not None and not df.empty:

                dados_df = df.tail(50).reset_index()

                socketio.emit("dados", {
                    "sinal": sinal,
                    "suporte": to_float(suporte),
                    "resistencia": to_float(resistencia),
                    "df": dados_df.to_dict(orient="records")
                })

        except Exception as e:
            print("Erro thread:", e)

        # ✔ correto para eventlet
        socketio.sleep(3)

# ---------------------------
# TROCAR ATIVO
# ---------------------------
@socketio.on("set_ativo")
def set_ativo(data):
    global ativo_global
    ativo_global = data["ativo"]

# ---------------------------
# START THREAD
# ---------------------------
def iniciar_thread():
    thread = threading.Thread(target=atualizar_dados)
    thread.daemon = True
    thread.start()

# ---------------------------
# RUN (RENDER)
# ---------------------------
if __name__ == "__main__":
    iniciar_thread()
    socketio.run(
        app,
        host="0.0.0.0",
        port=10000
    )
