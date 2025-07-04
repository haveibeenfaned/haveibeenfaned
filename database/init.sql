CREATE TABLE status
(
    process varchar(250) NOT NULL,
    status  boolean      NOT NULL DEFAULT FALSE
);

create table public.profiles
(
    id             integer generated always as identity,
    handle         varchar(250)            not null
        primary key,
    ig_url         varchar(250)            not null,
    onlyfans_url   varchar(250),
    fansly_url     varchar(250),
    linktree_url   varchar(250),
    beacons_url    varchar(250),
    lnk_url        varchar(250),
    allmylinks_url varchar(250),
    fname          varchar(250),
    funny_page     varchar(250),
    created_at     timestamp               not null,
    updated_at     timestamp default now() not null
);

alter table public.profiles
    owner to postgres;