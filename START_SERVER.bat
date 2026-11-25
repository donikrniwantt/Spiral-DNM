@echo off
setlocal EnableExtensions
set "ROOT=%~dp0"
set "EXE_DIR=%ROOT%exe"
set "MISSING=0"

echo Checking Dragon Nest Mobile server package...

for %%F in (audioserver.exe loginserver.exe dbserver.exe gameserver.exe gateserver.exe masterserver.exe controlserver.exe versionserver.exe) do (
    if not exist "%EXE_DIR%\%%F" (
        echo [MISSING] exe\%%F
        set "MISSING=1"
    )
)

for %%F in (audio_conf.xml login_conf.xml db_conf.xml gs_conf.xml gate_conf.xml ms_conf.xml ctrl_conf.xml version_conf.xml) do (
    if not exist "%EXE_DIR%\conf\%%F" (
        echo [MISSING] exe\conf\%%F
        set "MISSING=1"
    )
)

if "%MISSING%"=="1" (
    echo.
    echo ERROR: Required server files are missing. No server process was started.
    echo Restore the original build artifacts or compile the missing server binaries.
    exit /b 1
)

pushd "%EXE_DIR%" || exit /b 1
echo Starting server processes...
start "DNM Audio" /MIN audioserver.exe conf/audio_conf.xml
start "DNM Login" /MIN loginserver.exe conf/login_conf.xml
start "DNM Database" /MIN dbserver.exe conf/db_conf.xml
start "DNM Game" /MIN gameserver.exe conf/gs_conf.xml
start "DNM Gate" /MIN gateserver.exe conf/gate_conf.xml
start "DNM Master" /MIN masterserver.exe conf/ms_conf.xml
start "DNM Control" /MIN controlserver.exe conf/ctrl_conf.xml
start "DNM Version" /MIN versionserver.exe conf/version_conf.xml
popd

echo Startup commands submitted. Check each server log and listening port.
exit /b 0
