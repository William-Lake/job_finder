/* 

    Project .............: Job Finder
    Author ..............: William, Lake, Greg Beam
    Copyright ...........: Copyright (C) 2019 William Lake, Greg Beam
    License .............: GPL-3

    File ................: postgresql.sql
    Description .........: Creation script for the JobFinder project.
    Database Type .......: PostgreSQL v10 or later
    Version .............: 1.0.0

    Comments
    
        Creates the Database, Schema, and the user for managing.
        Table generation performed by JobFinder.

    Tool Requirments:

        * PostgreSQL v10 or above

    Installation
    
        * Clone the repository

            git clone https://github.com/KI7MT/job_finder
        
        * Change directories and run the sql script

            cd job_finder\data

            psql -v ON_ERROR_STOP=1 -U postgres -f postgresql.sql

    Development Activity and Coding

        Suffix Annotations
        _uq     = Unique Constraint
        _pkey   = Primary Key
        _fkey   = Foreign Key

*/

-- *****************************************************************************
--  BEGIN DATABASE CREATION
-- *****************************************************************************

\echo ''
\echo '---------------------------'
\echo 'Creating Job Finder DATABASE'
\echo '---------------------------'

-- Drop, and re-create schema
DROP DATABASE IF EXISTS job_finder;

-- Create New Schema
CREATE DATABASE job_finder;

-- Switching to new database so the following commands will work.
\c job_finder;

-- *****************************************************************************
--  BEGIN SCHEMA CREATION
-- *****************************************************************************

\echo ''
\echo '---------------------------'
\echo 'Creating Job Finder Schema'
\echo '---------------------------'

-- Create New Schema
CREATE SCHEMA jobs;

-- TABLE CREATION NOW PERFORMED BY JOB_FINDER

\echo ''
\echo '==========================='
\echo 'Creating jobs_admin User'
\echo '==========================='
\echo ''

-- NOTE: Some of these statements may seem redundant, but they're all necessary.

DROP USER IF EXISTS jobs_admin;

CREATE USER jobs_admin WITH ENCRYPTED PASSWORD 'jobs_admin';

GRANT ALL PRIVILEGES ON DATABASE job_finder TO jobs_admin;

GRANT ALL PRIVILEGES ON SCHEMA jobs TO jobs_admin;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA jobs TO jobs_admin;

GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA jobs TO jobs_admin;

GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA jobs TO jobs_admin;

ALTER DEFAULT PRIVILEGES IN SCHEMA jobs GRANT ALL PRIVILEGES ON TABLES TO jobs_admin;

ALTER DEFAULT PRIVILEGES IN SCHEMA jobs GRANT ALL PRIVILEGES ON SEQUENCES TO jobs_admin;

ALTER DEFAULT PRIVILEGES IN SCHEMA jobs GRANT ALL PRIVILEGES ON FUNCTIONS TO jobs_admin;

GRANT SELECT ON ALL TABLES IN SCHEMA PUBLIC TO jobs_admin;