CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL
);

CREATE OR REPLACE FUNCTION create_user(
    p_username VARCHAR,
    p_password VARCHAR,
    p_email VARCHAR
) RETURNS INTEGER AS $$
DECLARE
    hashed_password VARCHAR(128);
BEGIN
    hashed_password := crypt(p_password, gen_salt('bf'));
    INSERT INTO users (username, password_hash, email) VALUES (p_username, hashed_password, p_email) RETURNING id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION authenticate_user(
    p_username VARCHAR,
    p_password VARCHAR
) RETURNS INTEGER AS $$
DECLARE
    user_id INTEGER;
    hashed_password VARCHAR(128);
BEGIN
    SELECT id, password_hash INTO user_id, hashed_password FROM users WHERE username = p_username;
    IF hashed_password IS NULL THEN
        RETURN NULL;
    END IF;
    IF crypt(p_password, hashed_password) = hashed_password THEN
        RETURN user_id;
    ELSE
        RETURN NULL;
    END IF;
END;
$$ LANGUAGE plpgsql;

