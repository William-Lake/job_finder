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

/*
None of these are currently used in JobFinder.
This is for a couple of reasons:

    - Views don't really work well with the PeeWee ORM. 
    They don't throw errors/cause issues, but there is some
    odd functionality. Here's what is happening:
    
        - View generated in db via this script.
        - models.py generated via pwiz, adding View model to it.
        - View deleted from database to test database generation.
        - View generated via PeeWee from models outlined in models.py
        - The result is a *table* in the database with the
        same name as the original view, but not the view itself.
    
    I'm not the end-all be-all expert in the PeeWee ORM, but after
    significant research I'm not certain this is something we
    can get around at the moment. The table generation is
    definitely something we'd want to use.

    - The amount of logic in job_finder doesn't fully justify
    views at the moment. It made sense previously, when we'd
    have to create a sql statement, pass that to
    a db management class with params, who would then manage
    the steps in executing the sql and creating the objects.
    However, now we're able to gather all the open jobs like so:

        Job.select().where(Job.date_closed == None)

    As a result, a lot of the need for views has melted away.
    That said, there may be some future use that will make
    having these initial views useful so I'm leaving them here
    both out of respect for the author and in case they have 
    a place in the future.
*/

/*
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
*/