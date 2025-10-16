-- Conectarse a PostgreSQL como superusuario y ejecutar:
CREATE DATABASE blacklist_db;
CREATE USER postgres WITH PASSWORD 'mysecretpassword';
GRANT ALL PRIVILEGES ON DATABASE blacklist_db TO postgres;