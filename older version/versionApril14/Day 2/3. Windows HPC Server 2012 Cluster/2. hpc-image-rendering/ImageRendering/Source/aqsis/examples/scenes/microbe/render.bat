@ECHO OFF

REM ***Compile shaders***

ECHO === Compiling Shader(s) ===
ECHO.
aqsl.exe "../../../shaders/displacement/micro_bumps.sl"
aqsl.exe "../../../shaders/surface/microscope.sl"
IF NOT ERRORLEVEL 0 GOTO error


REM ***Render files***

ECHO.
ECHO.
ECHO === Rendering File(s) ===
ECHO.
aqsis.exe -progress "microbe.rib"
IF ERRORLEVEL 0 GOTO end


REM ***Error reporting***

:error
ECHO.
ECHO.
ECHO An error occured, please read messages !!!
PAUSE
EXIT
:end
