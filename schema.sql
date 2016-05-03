create table widgets (
  id serial primary key,
  name varchar(63) not null,
  data text
);

create table users (
  id serial primary key,
  username varchar(63) unique not null,
  password_hash text,
  name text
);
