// please change this if any changes
// see requirements.txt for installation purposes

database:
db = project
Idhar username and password apna daal dena
username = root
password = test

table 1 = login
CREATE TABLE `login` (
`user` varchar(255) NOT NULL,
`pass` varchar(255) NOT NULL,
PRIMARY KEY (`user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

table 2 = property
CREATE TABLE `property` (
`plotid` int NOT NULL AUTO_INCREMENT,
`ownername` varchar(25) NOT NULL,
`size` int NOT NULL,
`price` int NOT NULL,
`typeofhouse` varchar(20) NOT NULL,
`address` varchar(255) NOT NULL,
`lastUpdated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
`city` varchar(45) NOT NULL,
PRIMARY KEY (`plotid`),
UNIQUE KEY `plotid_UNIQUE` (`plotid`)
) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

table 3 favorite
CREATE TABLE `favorite` (
`id` int NOT NULL AUTO_INCREMENT,
`favorite_id` int DEFAULT NULL,
`ownername` varchar(255) DEFAULT NULL,
`current_user` varchar(45) NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

table 4 ratings
CREATE TABLE `ratings` (
`rating_id` int NOT NULL AUTO_INCREMENT,
`plot_id` int NOT NULL,
`rating` float NOT NULL DEFAULT '0',
`owner` varchar(45) NOT NULL,
PRIMARY KEY (`rating_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

table 5 users
CREATE TABLE `users` (
  `username` varchar(255) NOT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`username`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

// below this tumko banana hai
// while adding path to the db for images make sure to use \\ instead of \ for path
table 3 - image
user_id varchar(255) nn pk (user id argv se aajayega in photos.py tujhe bas db se display karna hai)
image1 largeblob nn
image2 largeblob nn
image3 largeblob nn
image4 largeblob nn
image5 largeblob nn
