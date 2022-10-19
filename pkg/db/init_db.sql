ALTER USER postgres WITH PASSWORD '2cuYUi}DLKyddIvniv{sP0yuq';
SELECT 'CREATE DATABASE admin_bot'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'admin_bot')\gexec
