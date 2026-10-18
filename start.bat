@echo off
title Installation des modules Python
color 0B

echo ========================================
echo       INSTALLATION DES MODULES
echo ========================================
echo.

cd /d "%~dp0"

if not exist "requirements.txt" (
    echo [ERREUR] Fichier requirements.txt introuvable !
    pause
    exit /b
)

echo [INFO] Installation des modules en cours...
echo.

py -m pip install -r requirements.txt

echo.
if %errorlevel%==0 (
    echo [SUCCES] Tous les modules ont ete installes !
) else (
    echo [ERREUR] Une erreur est survenue !
)

echo.
pause