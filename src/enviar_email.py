import smtplib
from email.message import EmailMessage
import os

def enviar_email_com_pdfs_do_arquivo(lista_pdf_txt, destinatario):
    remetente = os.getenv("EMAIL_REMETENTE")
    senha_app = os.getenv("EMAIL_SENHA_APP")

    if not remetente or not senha_app:
        print("[ERRO] Remetente ou senha de app não encontrados nas variáveis de ambiente")
        return

    if not os.path.exists(lista_pdf_txt):
        print("[ERRO] Arquivo pdfs_gerados.txt não encontrado.")
        return

    with open(lista_pdf_txt, "r") as f:
        pdfs = [linha.strip() for linha in f.readlines() if linha.strip()]

    if not pdfs:
        print("[ERRO] Nenhum PDF encontrado para enviar.")
        return

    print(f"[INFO] Enviando de: {remetente}")
    print(f"[INFO] Enviando para: {destinatario}")
    print(f"[INFO] Anexos encontrados: {len(pdfs)}")

    msg = EmailMessage()
    msg["Subject"] = "Relatório de Ocupação - FOR & REC"
    msg["From"] = remetente
    msg["To"] = destinatario
    msg.set_content("Este é um email automático. Segue em anexo os relatórios de ocupação FOR e REC.")

    for pdf_path in pdfs:
        try:
            with open(pdf_path, "rb") as f:
                file_data = f.read()
                file_name = os.path.basename(pdf_path)
                msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)
            print(f"[INFO] Anexado: {file_name}")
        except Exception as e:
            print(f"[ERRO] Falha ao anexar {pdf_path}: {e}")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(remetente, senha_app)
            smtp.send_message(msg)
        print("📧 E-mail enviado com sucesso!")
    except Exception as e:
        print(f"[ERRO] Falha ao enviar o e-mail: {e}")

# Execução direta
if __name__ == "__main__":
    enviar_email_com_pdfs_do_arquivo("pdfs_gerados.txt", "alanealvess@gmail.com")