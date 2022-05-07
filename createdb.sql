create table users(
    id integer primary key,
    username text unique,
    password text
);