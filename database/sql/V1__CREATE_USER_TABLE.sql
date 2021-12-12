CREATE TABLE soc.users( 
	usersId UUID DEFAULT gen_random_uuid() PRIMARY KEY,
	username STRING NOT NULL UNIQUE,
	email STRING NOT NULL,
	INDEX (usersId, groupId)
);

CREATE TABLE soc.userPasswords (
  passwordHash STRING(128) NOT NULL,
  usersId UUID NOT NULL UNIQUE REFERENCES soc.users (usersId) ON DELETE CASCADE,
  INDEX (usersId,passwordHash)
);