# slate_connect.py

import keyring
import getpass
import pandas as pd
from sqlalchemy import create_engine

"""
Provides a secure and convenient interface for connecting to and querying a Slate CRM database using SQLAlchemy.

This module encapsulates functionality to manage database connections to Slate CRM, which is commonly used in 
educational institutions for admissions and enrollment management. It leverages the SQLAlchemy library for 
database interactions and pandas for returning query results in a DataFrame format. Security for database 
passwords is ensured through the use of the keyring library, which stores credentials securely in the system's 
keyring service.

Classes:
    SlateSQLConnection: Manages connections to the Slate CRM database and provides methods for executing 
                        queries and handling password security.

Examples:
    Creating a connection object and connecting to the database:
    >>> conn = SlateSQLConnection(username='my_username', database='my_database',
    ...                           hostname='my_hostname', port='my_port', driver='ODBC+Driver+17+for+SQL+Server')
    >>> conn.connect()

    Testing the database connection:
    >>> conn.test_connection()
    Connection test successful. The database connection is working.

    Executing a query and retrieving results in a DataFrame:
    >>> query = "SELECT * FROM applicants WHERE rownum <= 10"
    >>> df = conn.execute_query(query)
    >>> print(df)

    Resetting the password stored in the keyring for the user:
    >>> conn.reset_password()
    Enter the new password for my_username: 
    Password has been reset successfully.

Notes:
    - This module requires the `sqlalchemy`, `pandas`, and `keyring` libraries for database operations, 
      handling query results, and managing database passwords securely, respectively.
    - Passwords are managed through the keyring and not stored in plain text or within the script, enhancing 
      security by leveraging the system's keyring service.
    - An instance of `SlateSQLConnection` uses the provided credentials and connection details to create 
      a SQLAlchemy engine. This engine is then used to execute SQL queries against the Slate CRM database.
    - Before using this module, ensure the appropriate database driver is installed and configured on your 
      system. The connection string format used in `connect` method may need to be adjusted based on the 
      driver and database being used.
    - The `get_password` and `reset_password` methods facilitate secure password retrieval and updating, 
      enhancing user convenience by avoiding the need to hard-code sensitive information.
"""

class SlateSQLConnection:
    def __init__(self, username, database, hostname, port, driver):
        self.username = username
        self.database = database
        self.hostname = hostname
        self.port = port
        self.driver = driver
        self.engine = None

    def get_password(self):
        # Retrieve the password from the keyring
        password = keyring.get_password('SlateSQLConnection', self.username)
        if password is None:
            # Prompt the user to set the password if it's not found
            password = getpass.getpass(f"Enter the password for {self.username}: ")
            # Store the password in the keyring
            keyring.set_password('SlateSQLConnection', self.username, password)
        return password

    def reset_password(self):
        # Prompt the user to enter a new password
        new_password = getpass.getpass(f"Enter the new password for {self.username}: ")
        # Store the new password in the keyring
        keyring.set_password('SlateSQLConnection', self.username, new_password)
        print("Password has been reset successfully.")

    def connect(self):
        # Get the password
        password = self.get_password()
        
        # Create the connection URL
        connection_url = f"mssql+pyodbc://{self.username}:{password}@{self.hostname},{self.port}/{self.database}?driver={self.driver}&Encrypt=yes&TrustServerCertificate=Yes"

        # Create the engine
        self.engine = create_engine(connection_url)
        
    def execute_query(self, query):
        # Ensure we are connected
        if self.engine is None:
            self.connect()
        
        # Use pandas to execute the query and return a DataFrame
        df = pd.read_sql(query, self.engine)
        return df
    
    def test_connection(self):
        try:
            # Attempt to execute a simple query to test the connection
            self.execute_query("SELECT 1")  # This query works for many SQL databases, adjust if needed
            print("Connection test successful. The database connection is working.")
        except Exception as e:
            # Handle the exception if the connection test fails
            print(f"Connection test failed: {e}")