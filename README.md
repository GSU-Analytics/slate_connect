# Slate Connect

## Description
A secure and convenient interface for connecting to and querying a Slate CRM database using SQLAlchemy and pandas.

## Installation Instructions

### Remote Installation

This approach installs the package directly from the remote repository, which is useful for users who need to use the package without contributing to its development.

1. **Create a Conda Environment, Install Package, and Activate Environment**:
   Copy the `slate_connect.yaml` file to your local machine.

   ```yaml
   # slate_connect.yaml

   name: slate_connect
   channels:
   - defaults
   dependencies:
   - python=3.10
   - sqlalchemy
   - keyring
   - pandas
   - pyodbc
   ```

   Install the package by following these steps: 
   1. Ensure Conda is installed by typing `conda -v` in the command line.
   2. Create a new Conda environment using the `slate_connect.yaml` file with the following command:
      ```cmd
      conda env create -f slate_connect.yaml
      conda activate slate_connect
      ```

2. **Install the Package in an Existing Environment**:
   ```cmd
   pip install git+https://github.com/GSU-Analytics/slate_connect.git
   ```

3. **Update the Package in an Existing Environment**:
   ```cmd
   pip install --upgrade git+https://github.com/GSU-Analytics/slate_connect.git
   ```

### Local Installation

For local installation, especially if you plan to contribute to the package or need a development setup:

1. **Clone the Repository**:
   ```cmd
   git clone https://github.com/GSU-Analytics/slate_connect.git
   cd slate_connect
   ```

2. **Create and Activate the Conda Environment**:
   Use the `slate_connect.yaml` file to set up an environment with all necessary dependencies installed via Conda. Navigate to the directory containing `slate_connect.yaml`, or specify the full path to the file.

   ```cmd
   conda env create -f slate_connect.yaml
   conda activate slate_connect
   ```

3. **Install the Package Locally**:
   This step installs the current local version of the package into the Conda environment.
   ```cmd
   pip install .
   ```

## Usage

To establish a connection to a Slate CRM database using the `SlateSQLConnection` class, configure your connection parameters in the `config.py` file. Below is a guide on how to do that and then utilize the configuration to connect to your Slate CRM database.

### Configuring Connection Parameters

The `config.py` file contains essential attributes for setting up your Slate CRM database connection. Ensure you have correctly configured the following attributes:

- `username`: Your Slate CRM database username.
- `database`: The name of the Slate CRM database you are connecting to.
- `hostname`: The hostname of the Slate CRM server.
- `port`: The port number for the Slate CRM server.
- `driver`: The ODBC driver for SQL Server that you are using.

Here's an example of how to set up `config.py`:

```python
# config.py

# Slate CRM Connection details
username = "your_username_here"
database = "your_database_here"
hostname = "your_hostname_here"
port = "your_port_here"
driver = "ODBC+Driver+17+for+SQL+Server"
```

### Connecting to the Database

With your `config.py` file set up, you can use the `SlateSQLConnection` class to connect to your Slate CRM database. Below is a step-by-step example of importing your configuration and creating a database connection:

```python
# main.py
from slate_connect import SlateSQLConnection
from config import username, database, hostname, port, driver

# Create a connection instance with the configured parameters
slate_conn = SlateSQLConnection(username, database, hostname, port, driver)

# Test the Slate CRM database connection
slate_conn.test_connection()

# Now you can use `slate_conn` to perform database operations
```

### Important Notes

- Always ensure that the `username`, `database`, `hostname`, `port`, and `driver` attributes in `config.py` are updated with the correct information corresponding to your Slate CRM setup.
- Never commit sensitive information, such as your actual database credentials, to a public repository. It's recommended to use environment variables or a secure credential management system for handling sensitive data.
- If you encounter any issues with connecting to the Slate CRM database, verify that the appropriate ODBC driver is installed and configured on your system.

## Examples

See the `example.py` file for a simple example of how to use the `SlateSQLConnection` class to connect to a Slate CRM database and execute a query. This will fetch orientation status counts from the `form.response` table and save the results to a CSV file.

```python
# example.py

from slate_connect import SlateSQLConnection
from config import username, database, hostname, port, driver

query = """
-- Orientation status counts since April 1, 2024
SELECT
    COALESCE(r.[status], 'register') AS status,
    COUNT(*) AS status_count
FROM [form.response] r 
INNER JOIN [form] f ON (f.[id] = r.[form]) 
LEFT OUTER JOIN [form] fp ON (fp.[id] = f.[parent])
WHERE f.[type] = 'event' 
AND ISNULL(f.[scope], fp.[scope]) = 'application'
AND f.date > '2024-04-01'
AND COALESCE(r.[status], 'register') IN ('register', 'attend', 'noshow', 'cancel')
AND LOWER(f.category) LIKE '%orientation%'
AND r.[record] IS NOT NULL
GROUP BY COALESCE(r.[status], 'register')
ORDER BY status
"""

slate_conn = SlateSQLConnection(username, database, hostname, port, driver)
print("Connecting to Slate CRM database...")
df = slate_conn.execute_query(query)
print("Query executed successfully.")
print("Saving query results to CSV file...")
df.to_csv('example.csv', index=False)
print("Results saved to example.csv.")
```

For more information, refer to the examples provided in `slate_connect/slate_connect.py` for details on how to use this package.