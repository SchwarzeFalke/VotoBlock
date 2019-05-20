
CREATE DATABASE VotoBlock_DB;
USE VotoBlock_DB;
CREATE TABLE user
(
  electoral_key VARCHAR(25) PRIMARY KEY NOT NULL,
  password VARCHAR(25) NOT NULL,
  email VARCHAR(40) NOT NULL,
  privilages CHAR(1) NOT NULL,
  exist BOOLEAN NOT NULL
);
CREATE TABLE scrutineer
(
  electoral_key VARCHAR(25) NOT NULL,
  name VARCHAR(25) NOT NULL,
  middle_name VARCHAR(25),
  flastname VARCHAR(25) NOT NULL,
  mlastname VARCHAR(25),
  can_add BOOLEAN NOT NULL,
  can_delete BOOLEAN NOT NULL,
  can_consult BOOLEAN NOT NULL,
  FOREIGN KEY (electoral_key)
   REFERENCES user(electoral_key)
);
CREATE TABLE voter
(
  electoral_key VARCHAR(25) NOT NULL,
  name VARCHAR(25) NOT NULL,
  middle_name VARCHAR(25),
  flastname VARCHAR(25) NOT NULL,
  mlastname VARCHAR(25),
  address VARCHAR(50),
  birth_date DATE,
  FOREIGN KEY (electoral_key)
   REFERENCES user(electoral_key)
);
CREATE TABLE election (
   _id INT PRIMARY KEY AUTO_INCREMENT,
   period DATE NOT NULL,
   descript VARCHAR
(50) NOT NULL,
   begining DATETIME NOT NULL,
   ending DATETIME NOT NULL,
   result VARCHAR
(50)
 );
CREATE TABLE candidate
(
  electoral_key VARCHAR(25) NOT NULL,
  election_id INT NOT NULL,
  name VARCHAR(25) NOT NULL,
  middle_name VARCHAR(25),
  flastname VARCHAR(25) NOT NULL,
  mlastname VARCHAR(25),
  party VARCHAR(25) NOT NULL,
  candidacy VARCHAR(25) NOT NULL,
  status VARCHAR(1) NOT NULL,
  FOREIGN KEY (electoral_key)
   REFERENCES user(electoral_key),
  FOREIGN KEY (election_id)
   REFERENCES election(_id)
);
CREATE TABLE proposal
(
  candidate_key VARCHAR(25) NOT NULL,
  description VARCHAR(100) NOT NULL,
  FOREIGN KEY (candidate_key)
   REFERENCES candidate(electoral_key)
);
CREATE TABLE vote (
   _id INT PRIMARY KEY AUTO_INCREMENT,
   _data_block_pointer INT NOT NULL,
   _encrypted_info VARCHAR
(64)
 );
CREATE TABLE data_block (
   _id INT PRIMARY KEY AUTO_INCREMENT,
   _hash CHAR
(8) NOT NULL,
   _pointer INT NOT NULL
 );
