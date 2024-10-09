CREATE TABLE soc.eventTypes(
    eventtypeuuid UUID DEFAULT gen_random_uuid() UNIQUE PRIMARY KEY,
    eventname STRING NOT NULL
);

CREATE TABLE soc.events(
    eventsuuid UUID DEFAULT gen_random_uuid() UNIQUE PRIMARY KEY,
    usersId UUID NOT NULL REFERENCES soc.users (usersId),
    eventtypeuuid UUID NOT NULL REFERENCES soc.eventTypes (eventtypeuuid),
    dateofevent DATE NOT NULL,
    INDEX (usersId,dateofevent,eventtypeuuid)
);