@echo off

:start
	cls
	python -m robot test_socket.robot
	pause
	goto start