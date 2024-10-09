CREATE TABLE soc.userSettings (
  settingName STRING(128) NOT NULL,
  settingValue STRING(128) NOT NULL,
  usersId UUID NOT NULL UNIQUE REFERENCES soc.users (usersId) ON DELETE CASCADE,
  INDEX (usersId,settingName)
);