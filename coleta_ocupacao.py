import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
import io
import time
from pdf2image import convert_from_path

# Caminho correto do Poppler que você informou
poppler_path = r"C:\Users\Alane Souza\poppler-24.08.0\Library\bin"

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()
        await page.goto("http://192.168.100.5:8501/")

        # Login
        await page.wait_for_selector("#text_input_1")
        await page.fill("#text_input_1", "analise.ocupacao")
        await page.fill("#text_input_2", "@Asa@locadora4930@#$")
        await page.click("button[data-testid='stBaseButton-secondaryFormSubmit']")
        print("[INFO] Login realizado.")

        time.sleep(70)

        # FOR
        print("[INFO] Iniciando coleta da operação FOR...")
        await page.wait_for_selector("button[data-testid='stTab']:has-text('Mapa de Ocupação')")
        await page.click("button[data-testid='stTab']:has-text('Mapa de Ocupação')")
        print("[INFO] Aba 'Mapa de Ocupação' clicada.")
        print("[INFO] Aguardando 140 segundos para FOR...")
        time.sleep(140)

        pdf_bytes = await page.pdf(format="A3", landscape=True, print_background=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        page2_pdf_path_for = f"FOR_mapa_ocupacao_pagina2_{timestamp}.pdf"

        reader = PdfReader(io.BytesIO(pdf_bytes))
        if len(reader.pages) >= 1:
            writer = PdfWriter()
            writer.add_page(reader.pages[0])
            with open(page2_pdf_path_for, "wb") as f:
                writer.write(f)
            print(f"[INFO] PDF FOR gerado: {page2_pdf_path_for}")
        else:
            print("[WARN] PDF FOR não possui páginas suficientes.")

        # Converter FOR para JPG
        try:
            images_for = convert_from_path(page2_pdf_path_for, dpi=300, poppler_path=poppler_path)
            if images_for:
                img_for_path = page2_pdf_path_for.replace(".pdf", ".jpg")
                images_for[0].save(img_for_path, "JPEG")
                print(f"[INFO] FOR convertido para imagem: {img_for_path}")
            else:
                print("[ERRO] Nenhuma imagem gerada para FOR.")
        except Exception as e:
            print(f"[ERRO] Falha ao converter FOR: {e}")

        # REC
        print("[INFO] Alternando para operação REC...")
        await page.locator("div[data-baseweb='select']").click()
        await page.wait_for_selector("div.st-emotion-cache-qiev7j:has-text('RAC REC')")
        await page.locator("div.st-emotion-cache-qiev7j:has-text('RAC REC')").click()
        await page.wait_for_timeout(2000)

        await page.click("button[data-testid='stTab']:has-text('Mapa de Ocupação')")
        print("[INFO] Aba 'Mapa de Ocupação' reaberta para RAC REC.")
        print("[INFO] Aguardando 400 segundos para REC...")
        time.sleep(400)

        pdf_bytes_rec = await page.pdf(format="A3", landscape=True, print_background=True)
        timestamp_rec = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        page2_pdf_path_rec = f"REC_mapa_ocupacao_pagina2_{timestamp_rec}.pdf"

        reader_rec = PdfReader(io.BytesIO(pdf_bytes_rec))
        if len(reader_rec.pages) >= 1:
            writer_rec = PdfWriter()
            writer_rec.add_page(reader_rec.pages[0])
            with open(page2_pdf_path_rec, "wb") as f:
                writer_rec.write(f)
            print(f"[INFO] PDF REC gerado: {page2_pdf_path_rec}")
        else:
            print("[WARN] PDF REC não possui páginas suficientes.")

        # Converter REC para JPG
        try:
            images_rec = convert_from_path(page2_pdf_path_rec, dpi=300, poppler_path=poppler_path)
            if images_rec:
                img_rec_path = page2_pdf_path_rec.replace(".pdf", ".jpg")
                images_rec[0].save(img_rec_path, "JPEG")
                print(f"[INFO] REC convertido para imagem: {img_rec_path}")
            else:
                print("[ERRO] Nenhuma imagem gerada para REC.")
        except Exception as e:
            print(f"[ERRO] Falha ao converter REC: {e}")

        await browser.close()

        with open("pdfs_gerados.txt", "w") as f:
            f.write(f"{page2_pdf_path_for}\n")
            f.write(f"{page2_pdf_path_rec}\n")
        print("[INFO] Caminhos salvos em pdfs_gerados.txt.")

asyncio.run(run())
