--This file creates the main schema for listings, as well as the tables

--Create schema
CREATE SCHEMA listings;

--Drop tables if exist
DROP TABLE IF EXISTS listings.calendar;
DROP TABLE IF EXISTS listings.host_verification;
DROP TABLE IF EXISTS listings.hosts;
DROP TABLE IF EXISTS listings.listing_amenities;
DROP TABLE IF EXISTS listings.listing_complements;
DROP TABLE IF EXISTS listings.listings;
DROP TABLE IF EXISTS listings.neighbourhoods;
DROP TABLE IF EXISTS listings.reviews;

--Create tables with schema
CREATE TABLE listings.calendar (
  id BIGINT NOT NULL PRIMARY KEY,
  listing_id BIGINT NOT NULL,
  date DATE,
  available BOOLEAN,
  price NUMERIC(9, 2),
  adjusted_price NUMERIC(9, 2),
  minimum_nights INT,
  maximum_nights INT
);

CREATE TABLE listings.host_verification (
  id BIGINT NOT NULL PRIMARY KEY,
  host_id BIGINT NOT NULL,
  verification TEXT
);

CREATE TABLE listings.hosts (
  id BIGINT NOT NULL PRIMARY KEY,
  url TEXT,
  name TEXT,
  since DATE,
  location TEXT,
  about TEXT,
  response_time TEXT,
  response_rate NUMERIC(9, 2),
  acceptance_rate NUMERIC(9, 2),
  is_superhost BOOLEAN,
  thumbnail_url TEXT,
  picture_url TEXT,
  neighbourhood TEXT,
  listings_count INT,
  total_listings_count INT,
  has_profile_pic BOOLEAN,
  identity_verified BOOLEAN
);

CREATE TABLE listings.listing_amenities (
  id BIGINT NOT NULL PRIMARY KEY,
  listing_id BIGINT NOT NULL,
  amenity VARCHAR(200)
);

CREATE TABLE listings.listing_complements (
  id BIGINT NOT NULL PRIMARY KEY,
  listing_id BIGINT NOT NULL,
  minimum_minimum_nights INT,
  maximum_minimum_nights INT,
  minimum_maximum_nights INT,
  maximum_maximum_nights INT,
  minimum_nights_avg_ntm DECIMAL(19, 2),
  maximum_nights_avg_ntm DECIMAL(19, 2),
  has_availability BOOLEAN,
  availability_30 INT,
  availability_60 INT,
  availability_90 INT,
  availability_365 INT,
  calendar_last_scraped DATE,
  number_of_reviews INT,
  number_of_reviews_ltm INT,
  number_of_reviews_l30d INT,
  first_review DATE,
  last_review DATE,
  review_scores_rating DECIMAL(9, 2),
  review_scores_accuracy DECIMAL(9, 2),
  review_scores_cleanliness DECIMAL(9, 2),
  review_scores_checkin DECIMAL(9, 2),
  review_scores_communication DECIMAL(9, 2),
  review_scores_location DECIMAL(9, 2),
  review_scores_value DECIMAL(9, 2),
  instant_bookable BOOLEAN,
  calculated_host_listings_count INT,
  calculated_host_listings_count_entire_homes INT,
  calculated_host_listings_count_private_rooms INT,
  calculated_host_listings_count_shared_rooms INT,
  reviews_per_month DECIMAL(9, 2)
);

CREATE TABLE listings.listings (
  id BIGINT NOT NULL PRIMARY KEY,
  host_id BIGINT NOT NULL,
  listing_url TEXT,
  scrape_id BIGINT,
  date_last_scraped DATE,
  name TEXT,
  description TEXT,
  neighborhood_overview TEXT,
  picture_url TEXT,
  neighbourhood_id BIGINT NOT NULL,
  neighbourhood_typed TEXT,
  latitude DECIMAL(9, 2),
  longitude DECIMAL(9, 2),
  property_type TEXT,
  room_type TEXT,
  accommodates INT,
  bathrooms_text TEXT,
  bedrooms INT,
  beds INT,
  price DECIMAL(9, 2),
  minimum_nights INT,
  maximum_nights INT
);

CREATE TABLE listings.neighbourhoods (
  id BIGINT NOT NULL PRIMARY KEY,
  neighbourhood VARCHAR(200)
);

CREATE TABLE listings.reviews (
  id BIGINT NOT NULL PRIMARY KEY,
  listing_id BIGINT NOT NULL,
  date DATE,
  reviewer_id BIGINT,
  reviewer_name VARCHAR(200),
  comments TEXT
);

--Grant all privileges for manipulating data on the schema to the Faculty service user
GRANT ALL ON listings.calendar TO service_user_faculty;
GRANT ALL ON listings.host_verification TO service_user_faculty;
GRANT ALL ON listings.hosts TO service_user_faculty;
GRANT ALL ON listings.listing_amenities TO service_user_faculty;
GRANT ALL ON listings.listing_complements TO service_user_faculty;
GRANT ALL ON listings.listings TO service_user_faculty;
GRANT ALL ON listings.neighbourhoods TO service_user_faculty;
GRANT ALL ON listings.reviews TO service_user_faculty;
