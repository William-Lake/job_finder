/* 
  
    Project .............: Job Finder
    Author ..............: William, Lake, Greg Beam
    Copyright ...........: Copyright (C) 2019 William Lake, Greg Beam
    License .............: GPL-3

    File ................: postgresql_view.sql
    Description .........: Views for Job FInder job.<schema>
    Database Type .......: PostgreSQL v10 or later
    Version .............: 1.0.0

*/

--******************************************************************************
-- CREATE TABLE VIEWS
--******************************************************************************

\echo ''
\echo '==========================='
\echo 'Creating Views'
\echo '==========================='
\echo ''

-- View  : jobs.recipient_view
-- Usage : select * from jobs.recipient_view
\echo 'jobs.recipient_view'
CREATE OR REPLACE VIEW jobs.recipient_view AS
    SELECT 
        recipient.email AS "Email",
        recipient.data_added AS "Date Added"
    FROM jobs.recipient
    ORDER BY jobs.recipient.email;

-- View  : jobs.all_job_view
-- Usage : select * from jobs.job_view
\echo 'jobs.all_job_view'
CREATE OR REPLACE VIEW jobs.all_job_view AS
    SELECT 
        job.site_id AS "Site",
        job.content_num AS "Number",
        job.title AS "Title",
        job.dept AS "Department",
        job.site_url AS "Weblink",
        job.opened_date AS "Opened Date",
        job.closed_date AS "Closed Date"
    FROM jobs.job
    ORDER BY jobs.job.date_opened;

-- View  : jobs.all_job_view
-- Usage : select * from jobs.job_view
\echo 'jobs.open_job_view'
CREATE OR REPLACE VIEW jobs.open_job_view AS
    SELECT 
        job.site_id AS "Site",
        job.content_num AS "Number",
        job.title AS "Title",
        job.dept AS "Department",
        job.site_url AS "Weblink",
        job.opened_date AS "Opened Date",
        job.closed_date AS "Closed Date"
    FROM jobs.job
    WHERE job.closed_date = NULL
    ORDER BY jobs.job.date_opened;

-- View  : jobs.props_view
-- Usage : select * from jobs.props_view
\echo 'jobs.open_job_view'
CREATE OR REPLACE VIEW jobs.props_view AS
    SELECT 
        job.smtp AS "SMTP",
        job.port AS "Port",
        job.email AS "Email",
        job.pword AS "Password"
    FROM jobs.props
    ORDER BY jobs.email;


-- END view creation
