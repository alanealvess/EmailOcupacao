@echo off
cd /d C:\Users\Alane Souza\EmailOcupacao
start /min cmd /c "ngrok http 8501 --log=stdout > logs/ngrok_log.txt"
timeout /t 5 > nul
python src/extrair_ngrok_link.py
