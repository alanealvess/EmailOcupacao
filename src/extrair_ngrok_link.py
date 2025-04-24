# import time
# import re

# log_file = "logs/ngrok_log.txt"           # log gerado pelo ngrok
# saida = "logs/ngrok_url.txt"              # para onde vamos salvar a URL

# url = None
# tentativas = 0

# while tentativas < 20:  # tenta por 20 segundos
#     try:
#         with open(log_file, "r", encoding="utf-8") as f:
#             texto = f.read()
#             resultado = re.search(r"https://[a-z0-9\-]+\.ngrok\-free\.app", texto)
#             if resultado:
#                 url = resultado.group(0)
#                 break
#     except FileNotFoundError:
#         pass
#     time.sleep(1)
#     tentativas += 1

# if url:
#     with open(saida, "w", encoding="utf-8") as f:
#         f.write(url)
#     print(f"[INFO] URL do ngrok salva: {url}")
# else:
#     print("[ERRO] Não foi possível encontrar a URL do ngrok.")
