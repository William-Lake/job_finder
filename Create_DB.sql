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
    site_url TEXT
);