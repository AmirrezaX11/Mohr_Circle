@echo off
setlocal
title Mohr's Circle - EXE Builder

echo.
echo ==========================================
echo       Mohr's Circle EXE Builder
echo ==========================================
echo.

cd /d "%~dp0"

echo [1/4] Checking Python...
where py >nul 2>nul
if %errorlevel%==0 (
    set "PY=py"
) else (
    where python >nul 2>nul
    if %errorlevel%==0 (
        set "PY=python"
    ) else (
        echo.
        echo ERROR: Python is not installed or is not in PATH.
        echo Install Python from python.org and enable:
        echo "Add python.exe to PATH"
        echo.
        pause
        exit /b 1
    )
)

echo Python found.
echo.

echo [2/4] Installing PyInstaller and Pillow...
%PY% -m pip install --upgrade pyinstaller pillow
if errorlevel 1 (
    echo.
    echo ERROR: Could not install required packages.
    echo Check your Internet connection.
    echo.
    pause
    exit /b 1
)

echo.
echo [3/4] Building EXE...
%PY% -m PyInstaller --clean --noconfirm --onefile --windowed --name "Mohrs_Circle" --icon "mohrs_circle.ico" --add-data "a_clean_modern_vector_style_graphic_icon_illus.png;." "mohrs_circle.py"

if errorlevel 1 (
    echo.
    echo ==========================================
    echo BUILD FAILED
    echo ==========================================
    echo.
    echo The error above shows the reason.
    echo.
    pause
    exit /b 1
)

echo.
echo [4/4] DONE!
echo.
echo ==========================================
echo EXE created successfully:
echo.
echo %CD%\dist\Mohrs_Circle.exe
echo ==========================================
echo.
pause
