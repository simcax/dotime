CREATE TABLE soc.timedmeetgo(
    timedmeetgouuid UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    usersId UUID NOT NULL REFERENCES soc.users (usersId) ON DELETE CASCADE,
    timefrom TIMESTAMPTZ NOT NULL,
    timeto TIMESTAMPTZ NOT NULL,
    INDEX (timedmeetgouuid,usersId)
);

CREATE TABLE soc.activites(
    activitesuuid  UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    usersId UUID NOT NULL REFERENCES soc.users (usersId) ON DELETE CASCADE,
    activityname STRING NOT NULL,
    activitycode STRING NULL,
    INDEX (activitesuuid,usersId)
);

CREATE TABLE soc.ln_timemeetgo(
    timedmeetgouuid UUID NOT NULL REFERENCES soc.users (usersId) ON DELETE CASCADE,
    activitesuuid UUID NOT NULL REFERENCES soc.users (usersId) ON DELETE CASCADE,
    INDEX(timedmeetgouuid,activitesuuid)
)