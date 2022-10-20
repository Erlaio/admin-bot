ALTER USER postgres WITH PASSWORD '2cuYUi}DLKyddIvniv{sP0yuq';

CREATE TABLESPACE admin_bot_tbs LOCATION '/db';

CREATE DATABASE admin_bot WITH OWNER = 'postgres' TABLESPACE = 'admin_bot_tbs';

