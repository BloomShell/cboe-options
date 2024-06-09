@echo off
REM Help and Documentation
if "%1"=="-h" (
    echo Usage: %~n0 [options]
    echo Options:
    echo    -d        Display documentation
    exit /b
)

REM Run the Python script
python "C:\cboe-options\run.py" %*
