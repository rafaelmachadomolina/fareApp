--This file creates the main schema for listings, as well as the tables

--Create schema
CREATE SCHEMA model;

--Drop existing tables
DROP TABLE IF EXISTS model.predictions;

--Create results table
CREATE TABLE model.predictions (
  id SERIAL PRIMARY KEY,
  accommodates INT,
  bedrooms INT,
  ocupation_days INT,
  ocupation DECIMAL(19, 6),
  postcode VARCHAR(20),
  proximity_score DECIMAL(19, 6),
  seniority INT,
  bathroom_number DECIMAL(19, 2),
  min_nights INT,
  total_amenities INT,
  host_total_listings INT,
  room_type VARCHAR(50),
  predicted_fare DECIMAL(19, 2),
  customer_name vARCHAR(50),
  ref_date TIMESTAMP
);


--Grant all privileges for manipulating data on the schema to the Faculty service user
GRANT ALL ON SCHEMA model TO service_user_faculty;
GRANT ALL ON TABLE model.predictions TO service_user_faculty;
GRANT ALL ON ALL SEQUENCES IN SCHEMA model TO service_user_faculty; -- For incremental only
