@ECHO OFF

REM ***Render files***

ECHO === Rendering File(s) ===
ECHO.
aqsis.exe -progress "menger.rib"
IF ERRORLEVEL 0 GOTO end


REM ***Error reporting***

:error
ECHO.
ECHO.
ECHO An error occured, please read messages !!!
PAUSE
EXIT
:end
