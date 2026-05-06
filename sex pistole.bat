@echo off
setlocal
cd /d "%~dp0"

:: On définit les noms EXACTS que je vois sur ta vidéo
set PY_FOLDER=python-3.14.3-embed-amd64
set SCRIPT_NAME=lancement.py

:: On vérifie si le dossier Python existe
if not exist "%PY_FOLDER%\python.exe" (
    echo ERREUR : Le dossier %PY_FOLDER% ou le fichier python.exe est introuvable !
    pause
    exit
)

:: On lance et on attend de voir si une erreur s'affiche
"%PY_FOLDER%\python.exe" "%SCRIPT_NAME%"

echo.
echo Si tu vois ce message, c'est que le script s'est arrêté.
pause