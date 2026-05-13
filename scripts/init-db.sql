-- Smart Guardian Backend - Database Initialization
-- Runs automatically on first PostgreSQL container start

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

GRANT ALL ON SCHEMA public TO sgadmin;
