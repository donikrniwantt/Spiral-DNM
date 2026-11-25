@echo off
setlocal EnableExtensions

echo Stopping Dragon Nest Mobile server processes...
for %%F in (gateserver.exe audioserver.exe loginserver.exe versionserver.exe gameserver.exe masterserver.exe controlserver.exe dbserver.exe) do (
    taskkill /F /IM %%F >nul 2>&1
)
echo Stop commands completed.
exit /b 0
