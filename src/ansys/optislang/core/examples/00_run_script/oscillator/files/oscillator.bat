@ECHO OFF

:: Starting SLang in batch mode
"%OPTISLANG_HOME%\slang\bin\slang.exe" -b %INPUT_FILE1%

:: uncomment the following lines to wait for the outputfile
:: :file_check
:: IF EXIST %OUTPUT_FILE1% (GOTO file_exists) ELSE (PING 127.0.0.1 -w 200 -n 1 >NUL)
:: GOTO file_check
::
:: :file_exists

