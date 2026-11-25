@echo off
setlocal EnableExtensions
pushd "%~dp0" || exit /b 1

set "MYSQL_USER=root"
set "MYSQL_PASSWORD="
set "MYSQL_HOST=127.0.0.1"
set "SQL_FILES_DIR=DataBaseInits"

where mysql >nul 2>&1
if errorlevel 1 (
    echo Error: mysql.exe was not found in PATH. Install MySQL 8.0 client tools or add them to PATH.
    popd
    exit /b 1
)

if not exist "%SQL_FILES_DIR%\" (
    echo Error: Directory "%SQL_FILES_DIR%" does not exist.
    popd
    exit /b 1
)

for %%F in (
    "%SQL_FILES_DIR%\1. DragonNestOnlineDB.sql"
    "%SQL_FILES_DIR%\2. WorldDB.sql"
    "%SQL_FILES_DIR%\3. LoginDB.sql"
    "%SQL_FILES_DIR%\4. LogDB.sql"
    "%SQL_FILES_DIR%\5. InitServerData.sql"
) do (
    if not exist "%%~fF" (
        echo Error: Required SQL file is missing: %%~fF
        popd
        exit /b 1
    )
)

echo Executing database initialization scripts in dependency order...
for %%F in (
    "%SQL_FILES_DIR%\1. DragonNestOnlineDB.sql"
    "%SQL_FILES_DIR%\2. WorldDB.sql"
    "%SQL_FILES_DIR%\3. LoginDB.sql"
    "%SQL_FILES_DIR%\4. LogDB.sql"
    "%SQL_FILES_DIR%\5. InitServerData.sql"
) do (
    echo Executing: %%~nxF
    mysql --host="%MYSQL_HOST%" --user="%MYSQL_USER%" --password="%MYSQL_PASSWORD%" < "%%~fF"
    if errorlevel 1 (
        echo Error: Failed to execute %%~nxF. Initialization stopped.
        popd
        exit /b 1
    )
)

echo All SQL scripts executed successfully.
popd
exit /b 0
