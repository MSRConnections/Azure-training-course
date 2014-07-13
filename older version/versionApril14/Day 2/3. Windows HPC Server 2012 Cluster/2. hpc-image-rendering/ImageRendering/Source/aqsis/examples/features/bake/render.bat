@ECHO OFF

REM ***Compile shaders***

ECHO === Compiling Shader(s) ===
ECHO.
aqsl.exe "../../../shaders/imager/gradient.sl"
aqsl.exe "../../../shaders/surface/expensive.sl"
IF NOT ERRORLEVEL 0 GOTO error


REM ***Render files***

ECHO.
ECHO.
ECHO === Rendering File(s) ===
ECHO.
aqsis.exe -progress "bakesphere.rib"
IF NOT ERRORLEVEL 0 GOTO error


REM ***Compile textures***

ECHO.
ECHO.
ECHO === Compiling Texture(s) ===
ECHO.
teqser.exe -wrap=periodic -filter=mitchell -width=2.0 -bake=128 "sphere.bake.bake" "sphere.bake.tex"
IF NOT ERRORLEVEL 0 GOTO error


REM ***Render files***

ECHO.
ECHO.
ECHO === Rendering File(s) ===
ECHO.
aqsis.exe -progress "sphere.rib"
IF ERRORLEVEL 0 GOTO end


REM ***Error reporting***

:error
ECHO.
ECHO.
ECHO An error occured, please read messages !!!
PAUSE
EXIT
:end
