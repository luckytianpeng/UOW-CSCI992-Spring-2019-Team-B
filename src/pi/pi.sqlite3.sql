-- CSCI991 Project Spring 2019, UOW
-- Team B

-- Project Name: Pi

-- by: Peng Tian, 5354870, pt882@uowmail.edu.au, 2020-04-26

BEGIN TRANSACTION;

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
	`email`	TEXT,
	`password`	TEXT NOT NULL,
	`activecode`	TEXT NOT NULL UNIQUE,
	`activity`	INTEGER NOT NULL,
	PRIMARY KEY(`email`)
);

COMMIT;
