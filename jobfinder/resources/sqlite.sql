CREATE TABLE appdata(
    author      TEXT,
    copyright   TEXT,
    license     TEXT,
    version     TEXT,
    email       TEXT,
    status      TEXT
);
INSERT INTO appdata(author,copyright,license,version,email,status) VALUES
    ('Job Finder ',
    '2019',
    'GPLv3',
    '0.0.1',
    'ki7mt@yahoo.com',
    'Development'
);

CREATE TABLE recipient
(
    id INTEGER PRIMARY KEY,
    email TEXT,
    date_added INTEGER
);

CREATE TABLE job
(
    id INTEGER,
    site_id INTEGER,
    contest_num INTEGER,
    title TEXT,
    dept TEXT,
    site_url TEXT,
    date_opened INTEGER,
    date_closed INTEGER
);

CREATE TABLE props
(
    id INTEGER PRIMARY KEY,
    smtp VARCHAR(120) NOT NULL,
    port INTEGER NOT NULL,
    email VARCHAR(120) NOT NULL,
    pword VARCHAR(120) NOT NULL
);
