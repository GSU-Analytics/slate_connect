# Slate Connect

## Description
A secure and convenient interface for connecting to and querying a Slate CRM database using SQLAlchemy and pandas.

## Prerequisites

### ODBC Driver 17 for SQL Server

This package requires Microsoft's ODBC Driver 17 for SQL Server to be installed at the system level before creating the conda environment. This is a system driver, not a Python package, and must be installed separately.

#### macOS

Install via Homebrew:

```bash
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
HOMEBREW_ACCEPT_EULA=Y brew install msodbcsql17
```

Verify the driver is registered:

```bash
odbcinst -q -d -n "ODBC Driver 17 for SQL Server"
```

#### Windows

Download and run the installer from Microsoft:

1. Go to [Microsoft ODBC Driver for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
2. Download **ODBC Driver 17 for SQL Server** for Windows.
3. Run the installer and follow the prompts.

Verify the driver is registered by opening **ODBC Data Sources (64-bit)** from the Start menu and checking the **Drivers** tab.

## Installation Instructions

### Using uv (Recommended)

[uv](https://docs.astral.sh/uv/) is the recommended tool for managing the environment and installing this package. Install it with:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Remote Installation

Install directly from GitHub into a uv-managed environment:

```bash
uv pip install git+https://github.com/GSU-Analytics/slate_connect.git
```

#### Update

```bash
uv pip install --upgrade git+https://github.com/GSU-Analytics/slate_connect.git
```

#### Local Development

```bash
git clone https://github.com/GSU-Analytics/slate_connect.git
cd slate_connect
uv sync
uv pip install -e .
```

---

### Using Conda

A `slate_connect.yml` file is provided for users who prefer Conda.

#### Remote Installation

1. Copy the `slate_connect.yml` file to your local machine.

   ```yaml
   name: slate_connect
   channels:
     - defaults
   dependencies:
     - python=3.10
     - sqlalchemy
     - keyring
     - pandas
     - pip
     - pip:
       - pyodbc
   ```

2. Create and activate the environment:

   ```bash
   conda env create -f slate_connect.yml
   conda activate slate_connect
   pip install git+https://github.com/GSU-Analytics/slate_connect.git
   ```

#### Local Development

```bash
git clone https://github.com/GSU-Analytics/slate_connect.git
cd slate_connect
conda env create -f slate_connect.yml
conda activate slate_connect
pip install -e .
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