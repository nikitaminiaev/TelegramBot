create table users(
    id integer primary key NOT NULL,
    chat_id integer NOT NULL,
    name varchar(255),
    type_subscriptions integer DEFAULT 0,
);

create table links(
    id integer primary key autoincrement,
    link varchar(255),
    type integer DEFAULT 0,
    data BLOB NOT NULL UNIQUE
);
