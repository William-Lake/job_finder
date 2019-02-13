/*
This script contains the minimal required amount of sql to run for 
PeeWee to generate the database tables.
    See: db_util.create_tables()

The tables cannot generated from the models unless the required database has already
been created.

PeeWee's model generator pwiz allows us to generate the models from an
existing database.
    See: http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#pwiz-a-model-generator

The command to do so is:

    python -m pwiz -e postgres -u jobs_admin -P -H 127.0.0.1 jobs > models.py

Where:

    -e postgres : Indicating the database type.
    -u jobs_admin  : Indicating the user for database access.
    -P : Indicating a password prompt should be used.
    -H 127.0.0.1 : Indicating the host.
    jobs : Indicating the database name.
    > models.py : Indicating where the output model data should be written to.

The following must be true in order for pwiz to successfully generate the model files:

    - The database/tables have already been created.
    - The tables are not in a schema.
    - The provided user has access to the database and each of the tables.
    - The provided user has SELECT access to the public schema tables.

The public schema tables are required for determining PK/FK relationships should
they ever be implemented.
*/

CREATE DATABASE jobs;

CREATE USER jobs_admin WITH ENCRYPTED PASSWORD 'jobs_admin';

GRANT ALL PRIVILEGES ON DATABASE jobs TO jobs_admin;

GRANT SELECT ON ALL TABLES IN SCHEMA PUBLIC TO jobs_admin;