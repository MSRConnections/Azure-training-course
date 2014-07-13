@ECHO OFF

REM ***Compile textures***

ECHO === Compiling Texture(s) ===
ECHO.
teqser.exe "grid.tif" "grid.tex"
IF NOT ERRORLEVEL 0 GOTO error


REM ***Compile shaders***

ECHO.
ECHO.
ECHO === Compiling Shader(s) ===
ECHO.
aqsl.exe "texmap.sl"
IF NOT ERRORLEVEL 0 GOTO error


REM ***Render files***

ECHO.
ECHO.
ECHO === Rendering File(s) ===
ECHO.
aqsis.exe -progress "layered.rib"
IF ERRORLEVEL 0 GOTO end


REM ***Error reporting***

:error
ECHO.
ECHO.
ECHO An error occured, please read messages !!!
PAUSE
EXIT
:end
