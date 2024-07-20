from setuptools import setup, find_packages

setup(
    name='your_project_name',  # Replace with your project name
    version='0.1.0',  # Initial release version
    description='A comprehensive project with advanced analytics and reporting features.',
    author='Your Name',  # Replace with your name
    author_email='your.email@example.com',  # Replace with your email
    url='https://github.com/yourusername/your_project_name',  # Replace with your project URL
    packages=find_packages(),  # Automatically find and include all packages in the project
    install_requires=[
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
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    entry_points={
        'console_scripts': [
            'your_project_name=your_project_name.cli:main',  # Replace with your CLI entry point
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
