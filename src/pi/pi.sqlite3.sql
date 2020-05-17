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

DROP TABLE IF EXISTS `file`;
CREATE TABLE IF NOT EXISTS `file` (
	`id`	TEXT,
	`email`	TEXT NOT NULL,
	`cell_type`	TEXT NOT NULL,
	`experiment_on`	TEXT NOT NULL,
	`plate_no`	TEXT NOT NULL,
	`files`	TEXT NOT NULL,
	`submit_time`	TEXT NOT NULL,
	`sirna`	TEXT NOT NULL,
	PRIMARY KEY(`id`),
	FOREIGN KEY(`email`) REFERENCES `user`(`email`) ON UPDATE CASCADE ON DELETE NO ACTION
);

COMMIT;
