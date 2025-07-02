CREATE TABLE status
(
    process varchar(250) NOT NULL,
    status  boolean      NOT NULL DEFAULT FALSE
);

CREATE TABLE user_histories(
    id INTEGER GENERATED ALWAYS AS IDENTITY,
    username varchar(250) NOT NULL PRIMARY KEY,
    funny_url varchar(250) NOT NULL,
    social_url varchar(250) NOT NULL,
    created_at timestamp,
    updated_at timestamp DEFAULT NOW()
);