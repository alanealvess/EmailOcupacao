import subprocess
import time
from datetime import datetime
import os

def log(mensagem):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log_execucao.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {mensagem}\n")
    print(f"[{timestamp}] {mensagem}")

log("Execução iniciada")

python_path = "C:\\Users\\Alane Souza\\Python\\Python313\\python.exe"

# --- Execução da coleta ---
try:
    log("Iniciando coleta de ocupação (coleta_ocupacao.py)")
    subprocess.run([python_path, "coleta_ocupacao.py"], check=True)
    log("Coleta concluída com sucesso")
except subprocess.CalledProcessError as e:
    log(f"Erro ao executar coleta_ocupacao.py: {e}")
    exit(1)

# --- Pausa antes do envio ---
log("Aguardando 10 segundos antes de enviar o e-mail...")
time.sleep(10)

# --- Envio do e-mail ---
try:
    log("Iniciando envio de e-mail (enviar_email.py)")
    subprocess.run([python_path, "enviar_email.py"], check=True)
    log("E-mail enviado com sucesso")
except subprocess.CalledProcessError as e:
    log(f"Erro ao executar enviar_email.py: {e}")
    exit(1)
    
    log("Execução finalizada\n" + "-"*60 + "\n")

# # --- Verificação de imagens antes do WhatsApp ---
# img_for = any(f.startswith("FOR") and f.endswith(".jpg") for f in os.listdir())
# img_rec = any(f.startswith("REC") and f.endswith(".jpg") for f in os.listdir())

# if img_for or img_rec:
#     try:
#         log("Iniciando envio de imagens pelo WhatsApp (enviar_whatsapp.py)")
#         subprocess.run([python_path, "enviar_whatsapp.py"], check=True)
#         log("Imagens enviadas com sucesso via WhatsApp")
#     except subprocess.CalledProcessError as e:
#         log(f"Erro ao executar enviar_whatsapp.py: {e}")
# else:
#     log("Nenhuma imagem JPG encontrada para envio via WhatsApp.")

