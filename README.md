# act-dental

This repository contains all setup files, ETL scripts, database integration, etc. for maintaining ACT Dental data architecture. Data is extracted from Pipedrive and loaded into Postgres database, which services Power BI for business reporting and analytics.

To initialize Postgres database and Pipedrive API, "pgdb.ini" file should be created with sections and keys defined as follows:

[postgres]
host=
database=
user=
password=

[pipedrive]
company_domain=
api_token=

For full pipeline to move data from Pipedrive API to Postgres databse, first open a new terminal. Then "cd" to the project (cd "ACT Dental"). Finally, execute "python ETL.py".
