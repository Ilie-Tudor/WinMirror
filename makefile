bash-cleanup:
	- rm -rf ./build
	- rm -rf ./dist

win-cleanup:
	- rmdir .\build\ -r
	- rmdir .\dist\ -r