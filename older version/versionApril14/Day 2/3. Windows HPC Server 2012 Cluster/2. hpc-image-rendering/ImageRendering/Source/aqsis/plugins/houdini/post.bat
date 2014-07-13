@ECHO OFF

REM ***System paths***

ECHO === System Path(s) ===
:start
ECHO.
SET /P HOUDINI_PATH="Please enter the installation path of Houdini: "
IF NOT EXIST %HOUDINI_PATH%\houdini\RIBtargets GOTO start
CD %HOUDINI_PATH%
IF NOT ERRORLEVEL 0 GOTO error


REM ***Compile shaders***

ECHO.
ECHO.
ECHO === Compiling Shader(s) ===
ECHO.
CD "houdini\ri_shaders"
aqsl.exe *.sl
IF ERRORLEVEL 0 GOTO end


REM ***Error reporting***

:error
ECHO.
ECHO.
ECHO An error occured, please read messages !!!
PAUSE
EXIT
:end
