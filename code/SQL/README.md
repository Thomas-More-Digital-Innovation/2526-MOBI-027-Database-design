# Exoskeleton Database Importer

A Python script to import exoskeleton data from Neo4j CSV exports into a MySQL database.

## Prerequisites

- Python 3.7 or higher
- MySQL database server
- CSV export files from Neo4j

## Setup Instructions

### 1. Clone or Download the Repository

```bash
# Navigate to your project directory
cd /path/to/your/project
```

### 2. Create a Virtual Environment

**On Windows:**
```bash
python -m venv venv
```

**On macOS/Linux:**
```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` appear at the beginning of your command prompt.

### 4. Install Required Dependencies

```bash
pip install -r requirements.txt
```

This will install all necessary packages:
- `mysql-connector-python`: MySQL database connector
- `python-dotenv`: Environment variable management

### 5. Configure Environment Variables

Create a `.env` file in the project root directory with your database credentials:

```env
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database_name
DB_PORT=3306
```

### 6. Create the Database Schema

Before importing data, you need to create the database tables. Run the provided SQL script:

**Using MySQL command line:**
```bash
mysql -u your_username -p your_database_name < build.sql
```

**Or using MySQL Workbench:**
1. Open MySQL Workbench
2. Connect to your database
3. Open the `build.sql` file
4. Execute the script

This will create all necessary tables and relationships.

### 7. Prepare CSV Files

Place your CSV export files in the project directory. The script expects these files:

- `neo4j_query_table_data_2025-10-15.csv`
- `neo4j_query_table_data_2025-10-15(2).csv`
- `neo4j_query_table_data_2025-10-15(3).csv`
- `neo4j_query_table_data_2025-10-16.csv`
- `neo4j_query_table_data_2025-10-16(2).csv`
- `neo4j_query_table_data_2025-10-22.csv`

If your files have different names, update the `CSV_FILES` dictionary in `full_import.py`.

### 8. Run the Import Script

```bash
python full_import.py
```

The script will:
- Connect to your MySQL database
- Process each CSV file in sequence
- Display progress and statistics for each import stage
- Show a final summary of all imported data

## What Gets Imported

The script processes data in 6 parts:

1. **Part 1**: Main Exo relationships (HAS_AIM, HAS_PROPERTY, ASSISTS_IN)
2. **Part 2**: Joint and constraint relationships (HAS_DOF, DOESNT_GO_WITH)
3. **Part 3**: DOF and AimType relationships (HAS_AS_MAIN_DOF, GIVES_RESISTANCE_IN, HAS_AIMTYPE)
4. **Part 4**: Part connections and limits (IS_CONNECTED_WITH, LIMITS_IN, HAS_SKNTYPE)
5. **Part 5**: Force transfer relationships (TRANSFERS_FORCES_FROM, TRANSFERS_FORCES_TO)
6. **Part 6**: Postural support relationships (GIVES_POSTURAL_SUPPORT_IN)

## Database Schema

The script requires a MySQL database with a specific schema. Use the provided `build.sql` file to create all necessary tables and relationships.

### Tables Created by build.sql:
- Exo
- Aim
- Dof
- JointT
- Part
- ExoProperty
- AimType
- StructureKinematicName
- StructureKinematicNameType

And relationship tables:
- HAS_AIM
- HAS_AIM_Structure
- HAS_PROPERTY
- ASSISTS_IN
- HAS_DOF
- DOESNT_GO_WITH
- HAS_AS_MAIN_DOF
- GIVES_RESISTANCE_IN
- GIVES_POSTURAL_SUPPORT_IN
- HAS_AIMTYPE
- IS_CONNECTED_WITH
- LIMITS_IN
- HAS_SKNTYPE
- TRANSFERS_FORCES_FROM
- TRANSFERS_FORCES_TO

## Troubleshooting

### Connection Error
If you get a database connection error:
- Verify your `.env` file has correct credentials
- Ensure MySQL server is running
- Check that the database exists

### CSV File Not Found
If you see "Warning: file not found":
- Verify CSV files are in the correct directory
- Check file names match exactly (including case)
- Update `CSV_FILES` dictionary if names differ

### Import Errors
If data fails to import:
- Check that database schema matches expected structure
- Verify CSV files have correct format
- Review error messages for specific issues

## Deactivating the Virtual Environment

When you're done, deactivate the virtual environment:

```bash
deactivate
```

## Project Structure

```
project/
│
├── venv/                          # Virtual environment (not in git)
├── .env                           # Database credentials (not in git)
├── .gitignore                     # Git ignore file
├── build.sql                      # Database schema creation script
├── full_import.py                 # Main import script
├── requirements.txt               # Python dependencies
├── README.md                      # This file
└── neo4j_query_table_data_*.csv  # CSV files (not in git)
```

## Dependencies

- `mysql-connector-python`: MySQL database connector
- `python-dotenv`: Environment variable management