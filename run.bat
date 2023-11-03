@echo off

set "venv_path=C:\YuSheng\Study\Seatech-Project\venv"

if exist "%venv_path%\Scripts\activate.bat" (
    call "%venv_path%\Scripts\activate.bat"
    echo Virtual environment activated.
) else (
    echo Virtual environment does not exist at the specified path.
)

flask --app flaskr run
