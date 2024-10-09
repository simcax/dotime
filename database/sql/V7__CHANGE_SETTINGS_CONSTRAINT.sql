DROP INDEX one_setting_per_user CASCADE;
ALTER TABLE soc.usersettings ADD CONSTRAINT one_setting_per_user UNIQUE (usersid,settingname);