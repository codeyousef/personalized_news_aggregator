import os
import sys
from importlib import import_module

def check_file_exists(file_path, file_type):
    exists = os.path.exists(file_path)
    print(f"{file_type}: {file_path} - {'✓' if exists else '✗'}")
    return exists

def check_module_imports(module_name):
    try:
        import_module(module_name)
        print(f"Module: {module_name} - ✓")
        return True
    except ImportError as e:
        print(f"Module: {module_name} - ✗ ({str(e)})")
        return False

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"Base directory: {BASE_DIR}")

# Check critical project files
required_files = [
    ('manage.py', 'Management script'),
    (os.path.join('news_aggregator', 'settings.py'), 'Settings'),
    (os.path.join('news_aggregator', 'urls.py'), 'URLs'),
    (os.path.join('accounts', 'models.py'), 'Accounts Models'),
    (os.path.join('news', 'models.py'), 'News Models'),
    (os.path.join('templates', 'base.html'), 'Base Template'),
]

files_exist = all(check_file_exists(os.path.join(BASE_DIR, file), file_type) for file, file_type in required_files)

# Check required modules
required_modules = ['django', 'requests']
modules_exist = all(check_module_imports(module) for module in required_modules)

# Print summary
print("\nValidation Summary:")
print(f"Required Files: {'All Present' if files_exist else 'Some Missing'}")
print(f"Required Modules: {'All Present' if modules_exist else 'Some Missing'}")

if files_exist and modules_exist:
    print("\nProject structure looks good! You can proceed with running the server.")
else:
    print("\nThere are issues with the project structure that need to be fixed before running the server.")