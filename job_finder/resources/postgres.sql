/* 

    Project .............: Job Finder
    Author ..............: William, Lake, Greg Beam
    Copyright ...........: Copyright (C) 2019 William Lake, Greg Beam
    License .............: GPL-3

    File ................: postgresql.sql
    Description .........: Enumeration Tables for R-DaaS Project
    Database Type .......: PostgreSQL v10 or later
    Version .............: 1.0.0

    Comments
    
        TODO: Add something relevant

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

-- Switching to your newly created database so the following commands will work.
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

-- *****************************************************************************
--  ADD DATABASE INFO
-- *****************************************************************************

--R-DaaS Informaiton Table
CREATE TABLE jobs.database_info
(
    id SERIAL,
    author VARCHAR (20),
    db_version VARCHAR(10),
    last_update DATE,
    CONSTRAINT database_info_id_pkey PRIMARY KEY (id)
);
INSERT INTO jobs.database_info (id, author, db_version, last_update)
VALUES(1, 'Greg Beam', '1.0.0', '2019-1-6');

-- *****************************************************************************
--  BEGIN TABLE CREATION
-- *****************************************************************************

\echo ''
\echo '==========================='
\echo 'Creating Tables'
\echo '==========================='
\echo ''
-- Recipent
\echo 'Creating Recipient Table'
CREATE TABLE jobs.recipient
(
    id SERIAL,
    email TEXT NOT NULL,
    data_added DATE NOT NULL,
    CONSTRAINT recipient_id_pkey PRIMARY KEY (id)
);

-- Job
\echo 'Creating Job Table'
CREATE TABLE jobs.job
(
    id SERIAL,
    site_id INTEGER NOT NULL,
    content_num INTEGER NOT NULL,
    title TEXT NOT NULL NOT NULL,
    dept TEXT NOT NULL NOT NULL,
    site_url TEXT NOT NULL,
    date_opened DATE NOT NULL,
    date_closed DATE,
    CONSTRAINT job_id_pkey PRIMARY KEY (id)
);

-- Prop
\echo 'Creating Prop Table'
CREATE TABLE jobs.prop
(
    id SERIAL,
    smtp VARCHAR (120) NOT NULL,
    port INTEGER NOT NULL,
    email VARCHAR NOT NULL,
    pword VARCHAR NOT NULL,
    is_selected BOOLEAN NOT NULL DEFAULT '0',
    CONSTRAINT prop_id_pkey PRIMARY KEY (id)
);

-- END table creation

--******************************************************************************
-- CREATE TABLE VIEWS
--******************************************************************************

\echo ''
\echo '==========================='
\echo 'Creating Views'
\echo '==========================='
\echo ''

-- View  : jobs.all_job_view
-- Usage : select * from jobs.job_view
\echo 'jobs.open_job_view'
CREATE OR REPLACE VIEW jobs.open_job_view AS
    SELECT *
    FROM jobs.job j
    WHERE j.date_closed IS NULL
    ORDER BY j.date_opened DESC;

-- END view creation

-- *****************************************************************************
--  BEGIN ROLE CREATION
-- *****************************************************************************

\echo ''
\echo '==========================='
\echo 'Creating jobs_admin User'
\echo '==========================='
\echo ''

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