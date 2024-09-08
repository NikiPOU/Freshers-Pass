CREATE TABLE IF NOT EXISTS tutor_group (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fresher_profile (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    tutor_group_id INTEGER REFERENCES tutor_group(id),
    CHECK (tutor_group_id IS NOT NULL),
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    points INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS tutor_profile (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    tutor_group_id INTEGER REFERENCES tutor_group(id),
    CHECK (tutor_group_id IS NOT NULL),
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS challenge_post (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    deadline TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'incomplete' CHECK (status IN ('incomplete', 'complete')),
    points_awarded INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS challenge_completion (
    id SERIAL PRIMARY KEY,
    fresher_id INTEGER REFERENCES fresher_profile(id),
    challenge_id INTEGER REFERENCES challenge_post(id),
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO tutor_group (name) VALUES ('Group 1');
INSERT INTO tutor_group (name) VALUES ('Group 2');
INSERT INTO tutor_group (name) VALUES ('Group 3');
INSERT INTO tutor_group (name) VALUES ('Group 4');
INSERT INTO tutor_group (name) VALUES ('Group 5');
INSERT INTO tutor_group (name) VALUES ('Group 6');
INSERT INTO tutor_group (name) VALUES ('Group 7');
INSERT INTO tutor_group (name) VALUES ('Group 8');
INSERT INTO tutor_group (name) VALUES ('Group 9');
INSERT INTO tutor_group (name) VALUES ('Group 10');
