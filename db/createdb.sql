create table users(
    id integer primary key NOT NULL,
    name varchar(255),
    subscriptions_nano boolean DEFAULT 0,
    subscriptions_ai boolean DEFAULT 0
);

create table links(
    id integer primary key autoincrement,
    link varchar(255),
    is_nano boolean DEFAULT 0,
    is_ai boolean DEFAULT 0,
    data BLOB NOT NULL UNIQUE
);
