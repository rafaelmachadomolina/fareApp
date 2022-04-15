--This file creates the main schema for listings, as well as the tables

--Create schema
CREATE SCHEMA city;

--Drop tables if exist
DROP TABLE IF EXISTS city.postcodes;
DROP TABLE IF EXISTS city.tfl_stations;

--Create tables with schema
CREATE TABLE city.postcodes (
  id BIGINT NOT NULL PRIMARY KEY,
  postcode VARCHAR(20),
  active BOOLEAN,
  latitude NUMERIC(19, 6),
  longitude NUMERIC(19, 6),
  neighbourhood_id BIGINT NOT NULL,
  postcode_area VARCHAR(20),
  district VARCHAR(100),
  postcode_district VARCHAR(20),
  constituency VARCHAR(100),
  postcode_url VARCHAR(20)
);

CREATE TABLE city.tfl_stations (
  id BIGINT NOT NULL PRIMARY KEY,
  name VARCHAR(50),
  description VARCHAR(200),
  latitude NUMERIC(19, 6),
  longitude NUMERIC(19, 6)
);

--Grant all privileges for manipulating data on the schema to the Faculty service user
GRANT ALL ON city.postcodes TO service_user_faculty;
GRANT ALL ON city.tfl_stations TO service_user_faculty;
