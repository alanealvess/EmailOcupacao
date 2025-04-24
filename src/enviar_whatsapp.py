import pywhatkit
import datetime
import os

numero = "+558195214238"

# Procura arquivos JPG gerados
arquivos = [f for f in os.listdir("output") if f.endswith(".jpg") and ("FOR" in f or "REC" in f)]

# Horário atual + 1 minuto
agora = datetime.datetime.now() + datetime.timedelta(minutes=1)
hora = agora.hour
minuto = agora.minute

# Envia cada imagem com legenda apropriada
for arquivo in sorted(arquivos):  # FOR antes de REC se possível
    if "FOR" in arquivo:
        legenda = "FOR - Ocupação diária"
    elif "REC" in arquivo:
        legenda = "REC - Ocupação diária"
    else:
        legenda = "Relatório de ocupação"

    caminho = os.path.abspath(os.path.join("output", arquivo))
    print(f"[INFO] Enviando {caminho} via WhatsApp com legenda: {legenda}")

    pywhatkit.sendwhats_image(
        receiver=numero,
        img_path=caminho,
        caption=legenda,
        wait_time=15,
        tab_close=True,
        close_time=3
    )

    # Aguarda 1 minuto entre os envios
    minuto += 1
