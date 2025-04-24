@echo off
cd /d C:\Users\Alane Souza\EmailOcupacao

:: Inicia ngrok e escreve a saída no log
start /min cmd /c "ngrok http 8501 --log=stdout > ngrok_log.txt"

:: Aguarda o ngrok subir
timeout /t 6 > nul

:: Extrai a URL e salva em ngrok_url.txt
powershell -Command ^
    "$log = Get-Content ngrok_log.txt -Raw; ^
    $match = $log -match 'https://[a-z0-9\\-]+\\.ngrok-free\\.app'; ^
    if ($match) { ^
        $url = $matches[0]; ^
        Set-Content ngrok_url.txt $url; ^
        echo URL encontrada: $url ^
    } else { ^
        echo [ERRO] URL do ngrok não encontrada. ^
    }"

exit
