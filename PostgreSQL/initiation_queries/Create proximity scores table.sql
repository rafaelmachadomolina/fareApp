--Query to create model table containing proximity scores

--Drop table if exists
DROP TABLE IF EXISTS model.proximity_score;

--Initialise table
CREATE TABLE model.proximity_score (
  id BIGINT NOT NULL PRIMARY KEY,
  postcode VARCHAR(20),
  neighbourhood_id BIGINT NOT NULL,
  postcode_url VARCHAR(20),
  score_stations DECIMAL(19, 6),
  active BOOLEAN
);

--Grant privileges to service user
GRANT ALL ON model.proximity_score TO service_user_faculty;
