CREATE TABLE user_profile (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    role TEXT CHECK (role IN ('fresher', 'tutor')) NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    profile_image_url TEXT,
    description TEXT,
    points INTEGER DEFAULT 0,
    tutor_group_id INTEGER REFERENCES tutor_group(id),
    CHECK ((role = 'fresher' AND tutor_group_id IS NOT NULL) OR role = 'tutor')
);

CREATE TABLE tutor_group (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    color VARCHAR(50),
    tutor_1_id INTEGER REFERENCES user_profile(id),
    tutor_2_id INTEGER REFERENCES user_profile(id)
);

CREATE TABLE tutor_profile (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    profile_image_url TEXT,
    description TEXT,
    tutor_group_id INTEGER REFERENCES tutor_group(id)
);

CREATE TABLE fresher_profile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES user_profile(id),
    profile_image_url TEXT,
    tutor_group_id INTEGER REFERENCES tutor_group(id)
);

CREATE TABLE tutor_post (
    id SERIAL PRIMARY KEY,
    tutor_id INTEGER REFERENCES tutor_profile(id),
    photo TEXT,
    title TEXT NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    location TEXT
);

CREATE TABLE challange_post (
    id SERIAL PRIMARY KEY,
    artist_id INTEGER REFERENCES user_profile(id),
    photo TEXT,
    title TEXT NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    location TEXT,
    status VARCHAR(50) DEFAULT 'pending',  -- New field for challenge status (pending, completed, denied)
    points_awarded INTEGER DEFAULT 0,      -- New field to store points awarded
    CHECK ((SELECT role FROM user_profile WHERE id = artist_id) = 'fresher')
);

CREATE TABLE feed (
    id SERIAL PRIMARY KEY,
    content_type TEXT CHECK (content_type IN ('tutor_post', 'challenge_post')) NOT NULL,
    content_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (content_id) REFERENCES tutor_post(id) ON DELETE CASCADE,
    FOREIGN KEY (content_id) REFERENCES challenge_post(id) ON DELETE CASCADE
);


CREATE TABLE event_schedule (
    id SERIAL PRIMARY KEY,
    challenge_id INTEGER REFERENCES challenge_post(id),
    show_time TIMESTAMP,
    location TEXT,
    external_calendar_url TEXT
);

