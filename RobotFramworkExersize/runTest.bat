@echo off

:start
	cls
	python -m robot fota_tests.robot
	pause
	goto start