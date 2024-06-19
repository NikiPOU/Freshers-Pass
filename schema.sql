
--CREATE TABLE table_name (
--  Column name + data type + constraints if any
--)




CREATE TABLE user_profile (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    gender VARCHAR(6),
    date_of_birth DATE,
    role TEXT CHECK (role IN ('artist', 'spectator')),
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    profile_image_url TEXT,
    description TEXT,
    following_count INTEGER DEFAULT 0,
    location TEXT

);

CREATE TABLE artist_followers (
    id SERIAL PRIMARY KEY,
    artist_id INTEGER REFERENCES user_profile(id),
    follower_id INTEGER REFERENCES user_profile(id)
)

CREATE TABLE user_followings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES user_profile(id),
    following_id INTEGER REFERENCES user_profile(id)
)

CREATE TABLE artist_post (
    id SERIAL PRIMARY KEY,
    artist_id INTEGER REFERENCES user_profile(id),
    photo TEXT,
    title TEXT NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    location TEXT

)

CREATE TABLE follower ( 
    following_user_id INTEGER REFERENCES user_profile(id),
    followed_artist_id INTEGER REFERENCES user_profile(id),
    PRIMARY KEY (following_user_id, followed_artist_id)
)

--only artists can post
--only artists can be followed
--artists have an artist profile
CREATE TABLE artist_profile (
    user_id INTEGER PRIMARY KEY REFERENCES user_profile(id),
    followers_count INTEGER DEFAULT 0,
    bio TEXT,
    CHECK ((SELECT role FROM user_profile WHERE id = user_id) = 'artist')
);

--spectators have a spectator profile
CREATE TABLE spectator_profile (
    user_id INTEGER PRIMARY KEY REFERENCES user_profile(id),
    bio TEXT,
    CHECK ((SELECT role FROM user_profile WHERE id = user_id) = 'spectator')
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    artist_id INTEGER REFERENCES user_profile(id),
    photo TEXT,
    title TEXT NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    location TEXT,
    CHECK ((SELECT role FROM user_profile WHERE id = artist_id) = 'artist')
);

CREATE TABLE feed (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE schedule (
    id SERIAL PRIMARY KEY,
    artwork_id INTEGER REFERENCES artworks(id),
    show_time TIMESTAMP,
    location TEXT
);

CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,
    artwork_id INTEGER REFERENCES artworks(id),
    spectator_id INTEGER REFERENCES spectators(user_id),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
