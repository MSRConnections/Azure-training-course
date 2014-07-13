@ECHO OFF

REM ***Compile shaders***

ECHO === Compiling Shader(s) ===
ECHO.
aqsl.exe "../../../shaders/displacement/dented.sl"
aqsl.exe "../../../shaders/light/shadowspot.sl"
IF NOT ERRORLEVEL 0 GOTO error


REM ***Render files***

ECHO.
ECHO.
ECHO === Rendering File(s) ===
ECHO.
aqsis.exe -progress "vase.rib"
IF ERRORLEVEL 0 GOTO end


REM ***Error reporting***

:error
ECHO.
ECHO.
ECHO An error occured, please read messages !!!
PAUSE
EXIT
:end
