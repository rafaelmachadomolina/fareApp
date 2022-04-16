--Query creates the base dataest for price modelling.

DROP TABLE IF EXISTS model.base_training_data;

--Save results on a different table
CREATE TABLE model.base_training_data AS

SELECT T1.id AS listing_id,
	T1.host_id,
	T1.neighbourhood_id,
	latitude,
	longitude,
	property_type,
	room_type,
	accommodates,
	bathrooms_text,
	bedrooms,
	beds,
	price AS price_per_night,
	minimum_nights,
	maximum_nights,
	total_amenities,
	has_wifi,
	has_kitchen,
	has_heating,
	instant_bookable,
	host_since,
	host_is_in_london,
	response_time,
	is_superhost,
	host_total_listings,
	host_has_profile_pic,
	identity_verified,
	verification_count,
	verification_phone,
	verification_email,
	verification_gov_id,
	neighbourhood,
	ROUND((total_nights - available_nights)*1.0 / total_nights, 3) AS ocupation
FROM
	(SELECT id,
		host_id,
		latitude,
		longitude,
		property_type,
		room_type,
		accommodates,
		bathrooms_text,
		bedrooms,
		beds,
		price,
		minimum_nights,
		maximum_nights,
	 	neighbourhood_id
	FROM listings.listings) T1
LEFT JOIN
	(SELECT listing_id,
		COUNT(*) AS total_amenities,
		SUM(CASE
		   WHEN amenity = 'Wifi' THEN 1
		   ELSE 0
		END) AS has_wifi,
		SUM(CASE
		   WHEN amenity = 'Kitchen' THEN 1
		   ELSE 0
		END) AS has_kitchen,
		SUM(CASE
		   WHEN amenity = 'Heating' THEN 1
		   ELSE 0
		END) AS has_heating
	FROM listings.listing_amenities
	GROUP BY listing_id) T2
ON T1.id = T2.listing_id
LEFT JOIN
	(SELECT listing_id,
		instant_bookable
	FROM listings.listing_complements) T3
ON T1.id = T3.listing_id
LEFT JOIN
	(SELECT id AS host_id,
		since AS host_since,
		CASE
			WHEN lower(location) LIKE '%london%' THEN 1
			ELSE 0
		END AS host_is_in_london,
		response_time,
		is_superhost,
		listings_count AS host_total_listings,
		has_profile_pic AS host_has_profile_pic,
		identity_verified
	FROM listings.hosts) T4
ON T1.host_id = T4.host_id
LEFT JOIN
	(SELECT host_id,
		COUNT(*) AS verification_count,
		SUM(CASE
			WHEN verification = 'phone' THEN 1
			ELSE 0
		END) AS verification_phone,
		SUM(CASE
			WHEN verification = 'email' THEN 1
			ELSE 0
		END) AS verification_email,
		SUM(CASE
			WHEN verification IN ('government_id', 'offline_government_id') THEN 1
			ELSE 0
		END) AS verification_gov_id
	FROM listings.host_verification
	GROUP BY host_id) T5
ON T1.host_id = T5.host_id
LEFT JOIN
	listings.neighbourhoods T6
ON T1.neighbourhood_id = T6.id
LEFT JOIN
	(SELECT listing_id,
		COUNT(*) AS total_nights,
		SUM(CASE
			WHEN available IS TRUE THEN 1
			ELSE 0
		END) AS available_nights
	FROM listings.calendar
	GROUP BY listing_id) T7
ON T1.id = T7.listing_id;

--Grant privileges to service user in Faculty
GRANT ALL ON model.base_training_data TO service_user_faculty;
