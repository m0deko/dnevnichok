CREATE TABLE IF NOT EXISTS maintable (

    id integer PRIMARY KEY AUTOINCREMENT,
    username text,
    password text NOT NULL,
    email text,
    surname text,
    realname text,
    second_name text,
    city text,
    school_num text,
    school_class text
);


