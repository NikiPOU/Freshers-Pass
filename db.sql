--there prolly shouldnt be a feed that
--shows whos done what, it should be that only
--tutors see the ranking
--so u cant also see others points but
--lets do so u see their profiles

--when new challanges are released, it shows
--as a banner

--honarable or blitz challanges? whoever does first
--it shows as a banner, and you can comment

--should tutors have points too (their own kind of system)?

--can only freshers comment on tutors and
--tutors comment on freshers

    --do default fresher when user signs up
    --tutors will be set via admin (me)


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

    points INTEGER DEFAULT 0,

    completed_challanges TEXT,
    incompleted_challanges TEXT,
    comments TEXT

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

CREATE TABLE fresher_profile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES user_profile(id),
    profile_image_url TEXT,
    tutor_group_id INTEGER REFERENCES tutor_group(id)
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

CREATE TABLE tutor_post (
    id SERIAL PRIMARY KEY,
    tutor_id INTEGER REFERENCES tutor_profile(id),
    title TEXT NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);

CREATE TABLE challange_post (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    deadline TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    location TEXT,
    status VARCHAR(50) DEFAULT 'pending',  --(pending, completed, denied)
    points_awarded INTEGER DEFAULT 0,      -- how many points its worth
    kide_link TEXT
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