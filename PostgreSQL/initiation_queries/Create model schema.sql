--This file creates the main schema for listings, as well as the tables

--Create schema
CREATE SCHEMA model;

--Grant all privileges for manipulating data on the schema to the Faculty service user
GRANT ALL ON SCHEMA model TO service_user_faculty;
