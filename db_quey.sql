-- Database: test_app_v1.0

-- DROP DATABASE IF EXISTS "test_app_v1.0";

CREATE DATABASE "test_app_v1.0"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

CREATE TABLE users (
	user_id INTEGER GENERATED ALWAYS AS IDENTITY,
	full_name VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255),
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOL
    PRIMARY KEY(user_id)
);

CREATE TABLE user_profile(
    profile_id INTEGER GENERATED ALWAYS AS IDENTITY,
    user_id INTEGER,
    dp BYTEA,
    PRIMARY KEY(profile_id),
    CONSTRAINT fk_user
      FOREIGN KEY(user_id) 
	  REFERENCES users(user_id)
)
