import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
import io
import time
import re
import subprocess

log_file = "logs/log_execucao.txt"

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_msg = f"[{timestamp}] {msg}"
    print(full_msg)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(full_msg + "\n")

async def run():
    url_local = "http://192.168.100.5:8501/"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()
        log("Acessando Mapa de Ocupação.")
        await page.goto(url_local)

        # Login
        await page.wait_for_selector("#text_input_1")
        await page.fill("#text_input_1", "analise.ocupacao")
        await page.fill("#text_input_2", "@Asa@locadora4930@#$")
        await page.click("button[data-testid='stBaseButton-secondaryFormSubmit']")
        log("Login realizado.")

        time.sleep(70)

        # FOR
        log("Iniciando coleta da operação FOR...")
        await page.wait_for_selector("button[data-testid='stTab']:has-text('Mapa de Ocupação')")
        await page.click("button[data-testid='stTab']:has-text('Mapa de Ocupação')")
        log("Aba 'Mapa de Ocupação' clicada para FOR.")
        log("Aguardando 140 segundos para FOR...")
        time.sleep(140)

        pdf_bytes = await page.pdf(format="A3", landscape=True, print_background=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        page2_pdf_path_for = f"output/FOR_mapa_ocupacao_pagina2_{timestamp}.pdf"

        reader = PdfReader(io.BytesIO(pdf_bytes))
        if len(reader.pages) >= 1:
            writer = PdfWriter()
            writer.add_page(reader.pages[0])
            with open(page2_pdf_path_for, "wb") as f:
                writer.write(f)
            log(f"PDF FOR gerado: {page2_pdf_path_for}")
        else:
            log("[WARN] PDF FOR não possui páginas suficientes.")

        # REC
        log("Alternando para operação REC...")
        await page.locator("div[data-baseweb='select']").click()
        await page.wait_for_selector("div.st-emotion-cache-qiev7j:has-text('RAC REC')")
        await page.locator("div.st-emotion-cache-qiev7j:has-text('RAC REC')").click()
        await page.wait_for_timeout(2000)

        await page.click("button[data-testid='stTab']:has-text('Mapa de Ocupação')")
        log("Aba 'Mapa de Ocupação' reaberta para RAC REC.")
        log("Aguardando 400 segundos para REC...")
        time.sleep(400)

        pdf_bytes_rec = await page.pdf(format="A3", landscape=True, print_background=True)
        timestamp_rec = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        page2_pdf_path_rec = f"output/REC_mapa_ocupacao_pagina2_{timestamp_rec}.pdf"

        reader_rec = PdfReader(io.BytesIO(pdf_bytes_rec))
        if len(reader_rec.pages) >= 1:
            writer_rec = PdfWriter()
            writer_rec.add_page(reader_rec.pages[0])
            with open(page2_pdf_path_rec, "wb") as f:
                writer_rec.write(f)
            log(f"PDF REC gerado: {page2_pdf_path_rec}")
        else:
            log("[WARN] PDF REC não possui páginas suficientes.")

        await browser.close()

        with open("logs/pdfs_gerados.txt", "w") as f:
            f.write(f"{page2_pdf_path_for}\n")
            f.write(f"{page2_pdf_path_rec}\n")
        log("Caminhos salvos em pdfs_gerados.txt.")

    # Envio de e-mail automático após geração dos PDFs
    try:
        log("Iniciando envio de e-mail...")
        subprocess.run(["python", "src/enviar_email.py"], check=True)
        log("E-mail enviado com sucesso.")
    except subprocess.CalledProcessError as e:
        log(f"[ERRO] Falha ao enviar o e-mail: {e}")

asyncio.run(run())
