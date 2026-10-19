# 451-autoclicker-v1 - Description rapide du programme.
# Copyright (C) 2026 uhqtools-on
# This file is part of 451-autoclicker-v1.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see https://www.gnu.org/licenses/.

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
