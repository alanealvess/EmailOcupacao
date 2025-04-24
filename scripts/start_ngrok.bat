@REM @echo off
@REM cd /d C:\Users\Alane Souza\EmailOcupacao

@REM :: Inicia ngrok e escreve a saída no log
@REM start /min cmd /c "ngrok http 8501 --log=stdout > ngrok_log.txt"

@REM :: Aguarda o ngrok subir
@REM timeout /t 6 > nul

@REM :: Extrai a URL e salva em ngrok_url.txt
@REM powershell -Command ^
@REM     "$log = Get-Content ngrok_log.txt -Raw; ^
@REM     $match = $log -match 'https://[a-z0-9\\-]+\\.ngrok-free\\.app'; ^
@REM     if ($match) { ^
@REM         $url = $matches[0]; ^
@REM         Set-Content ngrok_url.txt $url; ^
@REM         echo URL encontrada: $url ^
@REM     } else { ^
@REM         echo [ERRO] URL do ngrok não encontrada. ^
@REM     }"

@REM exit
