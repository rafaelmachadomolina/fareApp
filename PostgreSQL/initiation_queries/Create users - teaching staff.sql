--Create users in database

CREATE USER niallroche;
CREATE USER louisalecu;
CREATE USER walter_hernandez;

GRANT SELECT ON ALL TABLES IN SCHEMA listings TO niallroche;
GRANT SELECT ON ALL TABLES IN SCHEMA listings TO louisalecu;
GRANT SELECT ON ALL TABLES IN SCHEMA listings TO walter_hernandez;

GRANT SELECT ON ALL TABLES IN SCHEMA city TO niallroche;
GRANT SELECT ON ALL TABLES IN SCHEMA city TO louisalecu;
GRANT SELECT ON ALL TABLES IN SCHEMA city TO walter_hernandez;

GRANT SELECT ON ALL TABLES IN SCHEMA model TO niallroche;
GRANT SELECT ON ALL TABLES IN SCHEMA model TO louisalecu;
GRANT SELECT ON ALL TABLES IN SCHEMA model TO walter_hernandez;
