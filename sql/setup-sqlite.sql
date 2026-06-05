
-- User status updates
CREATE TABLE IF NOT EXISTS updates (
    id bigint,
    state bool,
    time timestamp
);

CREATE INDEX IF NOT EXISTS updates_id ON updates(id);
CREATE INDEX IF NOT EXISTS updates_time ON updates(time);


-- User info updates
CREATE TABLE IF NOT EXISTS user_updates (
    id bigint,
    time timestamp DEFAULT CURRENT_TIMESTAMP,
    username varchar(32),
    first_name varchar(255),
    last_name varchar(255),
    phone_number varchar(20)
);

CREATE INDEX IF NOT EXISTS user_updates_id ON user_updates(id);


-- Users
CREATE TABLE IF NOT EXISTS users (
    id bigint PRIMARY KEY,
    status_online bool,
    status_time timestamp,
    status_expires timestamp,
    username varchar(32),
    first_name varchar(255),
    last_name varchar(255),
    phone_number varchar(20)
);
