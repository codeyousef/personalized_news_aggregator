import os
import subprocess
import sys

def setup_django_project():
    """Set up Django project environment and run migrations."""
    # Check if virtual environment exists, create if not
    if not os.path.exists('.venv'):
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"])
    
    # Setup commands based on OS
    if os.name == 'nt':  # Windows
        python_path = ".venv\\Scripts\\python.exe"
        pip_path = ".venv\\Scripts\\pip.exe"
    else:  # Unix/Linux
        python_path = ".venv/bin/python"
        pip_path = ".venv/bin/pip"
    
    # Install requirements
    print("Installing requirements...")
    subprocess.run([pip_path, "install", "-r", "requirements.txt"])
    
    # Make migrations
    print("Creating database migrations...")
    subprocess.run([python_path, "manage.py", "makemigrations"])
    
    # Apply migrations
    print("Applying migrations...")
    subprocess.run([python_path, "manage.py", "migrate"])
    
    # Run tests
    print("Running tests...")
    subprocess.run([python_path, "manage.py", "test"])
    
    print("\nDjango project setup complete!")
    print("\nTo run the development server:")
    if os.name == 'nt':
        print(".venv\\Scripts\\python.exe manage.py runserver")
    else:
        print(".venv/bin/python manage.py runserver")

if __name__ == "__main__":
    setup_django_project()