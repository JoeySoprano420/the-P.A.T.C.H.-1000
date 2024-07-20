import subprocess
import sys

def install(package):
    """Install a package using pip."""
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def main():
    # List of required packages
    packages = [
        'Flask>=2.0.0',
        'pandas>=1.2.0',
        'openpyxl>=3.0.0',
        'flask_jwt_extended>=4.0.0',
        'apscheduler>=3.6.3',
        'requests>=2.25.1',
        'numpy>=1.21.0',
        'flask_cors>=3.0.10',
        'flask_mail>=0.9.1',
        'python-dotenv>=0.19.1',
        'mongoengine>=0.24.1',
    ]

    # Install each package
    for package in packages:
        install(package)

if __name__ == '__main__':
    main()
