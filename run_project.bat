@echo off
echo Setting up News Aggregator Project...

REM Create virtual environment if it doesn't exist
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment and install requirements
echo Activating virtual environment and installing requirements...
call .venv\Scripts\activate.bat
pip install -r requirements.txt

REM Run migrations
echo Running migrations...
python manage.py makemigrations accounts news
python manage.py migrate

REM Run tests
echo Running tests...
python manage.py test

REM Start server
echo Starting development server...
python manage.py runserver

pause