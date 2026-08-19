@echo off

:start
cls
python -m pytest -v
echo. 
echo press any key to run again
pause
goto start