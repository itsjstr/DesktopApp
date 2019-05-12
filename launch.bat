@echo off
node init.js
start cmd /c npm test
flask run
