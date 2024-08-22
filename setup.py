from setuptools import setup, find_packages

setup(
    name='slate_connect',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'keyring',
        'sqlalchemy',
        'pyodbc',
    ],
    author='Isaac Kerson',
    author_email='ikerson@gsu.edu',
    description='A secure and convenient interface for connecting to and querying a Slate CRM database using SQLAlchemy.',
    keywords='slate crm database connection pandas sqlalchemy',
    url='https://github.com/GSU-Analytics/slate_connect.git', 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
