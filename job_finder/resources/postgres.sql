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
--  BEGIN SCHEMA CREATION
-- *****************************************************************************

-- PeeWee doesn't support tables within a schema.

\echo ''
\echo '---------------------------'
\echo 'Creating Job Finder Schema'
\echo '---------------------------'

-- Drop, and re-create schema
DROP SCHEMA IF EXISTS jobs CASCADE;

-- Create New Schema
CREATE SCHEMA jobs;


DROP TABLE IF EXISTS jobs.database_info;
DROP TABLE IF EXISTS jobs.recipient;
DROP TABLE IF EXISTS jobs.job;
DROP TABLE IF EXISTS jobs.prop;

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

-- *****************************************************************************
--  BEGIN ROLE CREATION
-- *****************************************************************************

\echo ''
\echo '==========================='
\echo 'Creating jobs_admin User'
\echo '==========================='
\echo ''

CREATE USER jobs_admin WITH ENCRYPTED PASSWORD 'jobs_admin';

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA jobs TO jobs_admin;

GRANT SELECT ON ALL TABLES IN SCHEMA PUBLIC TO jobs_admin;