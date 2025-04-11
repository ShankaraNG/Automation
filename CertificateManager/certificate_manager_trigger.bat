@echo off

:: Certificate Manager Batch Script
:: Script by Shankar
:: Date: 09-AUG-2023

:: Function 1: Using OpenSSL to check certificate
:check_cert_openssl
set HOST=%1
set PORT=%2
set inputpath=%3
set outputpath=%4
set certname=%5
set keyname=%6
set keystorecheck=%7
set keystorename=%8
set truststorecheck=%9
set truststorename=%10

echo Checking certificate using OpenSSL for %HOST%:%PORT%
echo | openssl s_client -connect %HOST%:%PORT% <nul 2^>nul | openssl x509 -noout -issuer -subject -dates > certificateoutput.txt

for /f "tokens=2 delims==" %%i in ('findstr /c:"notAfter" certificateoutput.txt') do set expirydate=%%i
for /f "tokens=1-3" %%a in ("%expirydate%") do set expirydate_formatted=%%a %%b %%c

:: Convert expiry date to seconds
for /f "tokens=1,2,3,4" %%a in ('echo %expirydate_formatted%') do (
    set expirydateinseconds=%%a
)

:: Get current date in seconds
for /f "tokens=1,2,3" %%a in ('date /t') do set currentdateinseconds=%%a

:: Calculate time left until expiry
set /a seconds_expire=%expirydateinseconds% - %currentdateinseconds%
set /a covert_todays=%seconds_expire% / 86400

if "%covert_todays%" == "10" (
    :: Mention the Path to your Python Script
    python certificateDriver.py

    if "%keystorecheck%" == "False" (
        :: Backup old cert files
        cd "%outputpath%"
        mkdir certbackup_%date:~6,4%-%date:~3,2%-%date:~0,2%
        chmod 775 certbackup_%date:~6,4%-%date:~3,2%-%date:~0,2%
        copy * "%outputpath%\certbackup_%date:~6,4%-%date:~3,2%-%date:~0,2%\"
        move "%certname%" "%outputpath%"
        move "%keyname%" "%outputpath%"
        echo certificate and key are moved to the required path
    ) else if "%keystorecheck%" == "True" (
        cd "%outputpath%"
        mkdir certbackup_%date:~6,4%-%date:~3,2%-%date:~0,2%
        chmod 775 certbackup_%date:~6,4%-%date:~3,2%-%date:~0,2%
        copy * "%outputpath%\certbackup_%date:~6,4%-%date:~3,2%-%date:~0,2%\"
        move "%keystorename%" "%outputpath%"
        echo Keystore is moved to the required path
    ) else if "%keystorecheck%" == "True" and "%truststorecheck%" == "True" (
        cd "%outputpath%"
        mkdir certbackup_%date:~6,4%-%date:~3,2%-%date:~0,2%
        chmod 775 certbackup_%date:~6,4%-%date:~3,2%-%date:~0,2%
        copy * "%outputpath%\certbackup_%date:~6,4%-%date:~3,2%-%date:~0,2%\"
        move "%keystorename%" "%outputpath%"
        move "%truststorename%" "%outputpath%"
        echo Trust Store and Keystore are moved to the required path
    ) else (
        echo Invalid Input for certificate check
    )
) else (
    echo There is still time for the certificate to expire
)

exit /b

:: Function 2: Using cURL to check certificate
:check_cert_curl
set URL=%1
set inputpath=%2
set outputpath=%3
set certname=%4
set keyname=%5
set keystorecheck=%6
set keystorename=%7
set truststorecheck=%8
set truststorename=%9

echo Checking certificate using curl for %URL%
curl -svo nul -k "%URL%" 2>&1 | findstr /i "subject: issuer: start date: expire date: SSL connection using" > certificateoutput.txt

for /f "tokens=2 delims=:" %%i in ('findstr /i "expire date:" certificateoutput.txt') do set expirydate=%%i
for /f "tokens=1-3" %%a in ("%expirydate%") do set expirydate_formatted=%%a %%b %%c

:: Convert expiry date to seconds
for /f "tokens=1,2,3,4" %%a in ('echo %expirydate_formatted%') do (
    set expirydateinseconds=%%a
)

:: Get current date in seconds
for /f "tokens=1,2,3" %%a in ('date /t') do set currentdateinseconds=%%a

:: Calculate time left until expiry
set /a seconds_expire=%expirydateinseconds% - %currentdateinseconds%
set /a covert_todays=%seconds_expire% / 86400

if "%covert_todays%" == "10" (
    :: Mention the Path to your Python Script
    python certificateDriver.py

    if "%keystorecheck%" == "False" (
        :: Backup old cert files
        cd "%outputpath%"
        mkdir certbackup_%date:~6,4%-%date:~3,2%-%date:~0,2%
        chmod 775 certbackup_%date:~6,4%-%date:~3,2%-%date:~0,2%
        copy * "%outputpath%\certbackup_%date:~6,4%-%date:~3,2%-%date:~0,2%\"
        move "%certname%" "%outputpath%"
        move "%keyname%" "%outputpath%"
        echo certificate and key are moved to the required path
    ) else if "%keystorecheck%" == "True" (
        cd "%outputpath%"
        mkdir certbackup_%date:~6,4%-%date:~3,2%-%date:~0,2%
        chmod 775 certbackup_%date:~6,4%-%date:~3,2%-%date:~0,2%
        copy * "%outputpath%\certbackup_%date:~6,4%-%date:~3,2%-%date:~0,2%\"
        move "%keystorename%" "%outputpath%"
        echo Keystore is moved to the required path
    ) else if "%keystorecheck%" == "True" and "%truststorecheck%" == "True" (
        cd "%outputpath%"
        mkdir certbackup_%date:~6,4%-%date:~3,2%-%date:~0,2%
        chmod 775 certbackup_%date:~6,4%-%date:~3,2%-%date:~0,2%
        copy * "%outputpath%\certbackup_%date:~6,4%-%date:~3,2%-%date:~0,2%\"
        move "%keystorename%" "%outputpath%"
        move "%truststorename%" "%outputpath%"
        echo Trust Store and Keystore are moved to the required path
    ) else (
        echo Invalid Input for certificate check
    )
) else (
    echo There is still time for the certificate to expire
)

exit /b

:: User Input section
set URL=https://google.co.in:443
set BackendCheck=False
set inputpath=C:\app\monitoring\shankar\
set outputpath=C:\app\monitoring\shankar\
set certname=C:\app\monitoring\shankar\shankar.cer
set keyname=C:\app\monitoring\shankar\shankar.key
set keystorecheck=True
set keystorename=C:\app\monitoring\shankar\shankar.jks
set truststorecheck=True
set truststorename=C:\app\monitoring\shankar\shankar_trust.jks

:: Check if the URL starts with "https://"
if "%URL%" == https://* (
    echo URL starts with https://
    call :check_cert_curl "%URL%" "%inputpath%" "%outputpath%" "%certname%" "%keyname%" "%keystorecheck%" "%keystorename%" "%truststorecheck%" "%truststorename%"
) else if "%URL%" neq https://* if "%BackendCheck%" == "False" (
    echo URL does NOT start with https://
    set URL=https://%URL%
    call :check_cert_curl "%URL%" "%inputpath%" "%outputpath%" "%certname%" "%keyname%" "%keystorecheck%" "%keystorename%" "%truststorecheck%" "%truststorename%"
) else if "%URL%" neq https://* if "%BackendCheck%" == "True" (
    set host=%URL%
    set port=%URL%
    call :check_cert_openssl "%host%" "%port%" "%inputpath%" "%outputpath%" "%certname%" "%keyname%" "%keystorecheck%" "%keystorename%" "%truststorecheck%" "%truststorename%"
) else (
    echo Invalid URL
)

