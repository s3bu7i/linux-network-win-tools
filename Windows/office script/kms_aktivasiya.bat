@echo off
setlocal

echo ==============================
echo  OFFICE KMS ACTIVATION SCRIPT
echo ==============================

:: Navigate to the Office installation folder
if exist "C:\Program Files\Microsoft Office\Office16" (
    cd /d "C:\Program Files\Microsoft Office\Office16"
) else if exist "C:\Program Files (x86)\Microsoft Office\Office16" (
    cd /d "C:\Program Files (x86)\Microsoft Office\Office16"
) else (
    echo Office 2016/2019/2021 not found on this system.
    pause
    exit /b
)

:: Get license name
for /f "tokens=2 delims==" %%i in ('cscript ospp.vbs /dstatus ^| findstr /i "LICENSE NAME"') do (
    set "licname=%%i"
)

:: Clean up formatting
set "licname=%licname:~1%"

echo Detected license: %licname%

:: Set the appropriate KMS key
set "kmskey="
echo Checking license version...

echo %licname% | findstr /i "Office 2021" >nul && set "kmskey=FXYTK-NJJ8C-GB6DW-3DYQT-6F7TH"
echo %licname% | findstr /i "Office 2019" >nul && set "kmskey=NMMKJ-6RK4F-KMJVX-8D9MJ-6MWKP"
echo %licname% | findstr /i "Office 2016" >nul && set "kmskey=XQNVK-8JYDB-WJ9W3-YJ8YR-WFG99"

if "%kmskey%"=="" (
    echo No matching KMS key found or this is not a Volume License (VL) edition.
    pause
    exit /b
)

echo Applying KMS key: %kmskey%

:: Remove previous key (if any)
for /f "tokens=3 delims=:" %%i in ('cscript ospp.vbs /dstatus ^| findstr /i "Last 5 characters"') do (
    set "lastkey=%%i"
)

if defined lastkey (
    echo Removing old product key...
    cscript ospp.vbs /unpkey:%lastkey: =%
)

:: Install new KMS key
echo Installing new KMS client key...
cscript ospp.vbs /inpkey:%kmskey%

:: Configure KMS host and port
echo Setting KMS server...
cscript ospp.vbs /sethst:e8.us.to
cscript ospp.vbs /setprt:1688

:: Activate Office
echo Activating Office...
cscript ospp.vbs /act

echo -------------------------------------
echo Activation process completed.
pause
endlocal
exit /b
