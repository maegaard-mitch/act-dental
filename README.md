# act-dental

This repository contains all setup files, ETL scripts, database integration, etc. for maintaining ACT Dental data architecture. Data is extracted from Pipedrive and loaded into Postgres database, which services Power BI for business reporting and analytics.

To initialize Postgres database, "pgdb.ini" file should be created with parameters specifying host, database name, username, and password. The same file can be used to store Pipedrive API connection information.
