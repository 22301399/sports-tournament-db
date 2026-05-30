DROP TABLE IF EXISTS match_results CASCADE;
DROP TABLE IF EXISTS matches CASCADE;
DROP TABLE IF EXISTS team_players CASCADE;
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS teams CASCADE;
DROP TABLE IF EXISTS tournaments CASCADE;
DROP TABLE IF EXISTS venues CASCADE;
DROP TABLE IF EXISTS user_groups CASCADE;
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE user_groups (
    group_id      SERIAL PRIMARY KEY,
    group_name    VARCHAR(50) NOT NULL UNIQUE,
    description   TEXT,
    can_manage_tournaments BOOLEAN DEFAULT FALSE,
    can_manage_teams       BOOLEAN DEFAULT FALSE,
    can_manage_players     BOOLEAN DEFAULT FALSE,
    can_view_only          BOOLEAN DEFAULT TRUE,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    user_id       SERIAL PRIMARY KEY,
    username      VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email         VARCHAR(100) NOT NULL UNIQUE,
    full_name     VARCHAR(100) NOT NULL,
    group_id      INTEGER NOT NULL REFERENCES user_groups(group_id),
    is_active     BOOLEAN DEFAULT TRUE,
    last_login    TIMESTAMP,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT email_format CHECK (email LIKE '%@%.%')
);

CREATE TABLE venues (
    venue_id      SERIAL PRIMARY KEY,
    venue_name    VARCHAR(100) NOT NULL,
    city          VARCHAR(100) NOT NULL,
    country       VARCHAR(100) NOT NULL DEFAULT 'Turkey',
    capacity      INTEGER CHECK (capacity > 0),
    surface_type  VARCHAR(50) CHECK (surface_type IN ('Grass', 'Artificial Turf', 'Clay', 'Hard Court', 'Indoor')),
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tournaments (
    tournament_id   SERIAL PRIMARY KEY,
    tournament_name VARCHAR(150) NOT NULL,
    sport_type      VARCHAR(50) NOT NULL CHECK (sport_type IN ('Football', 'Basketball', 'Tennis', 'Volleyball', 'Swimming')),
    start_date      DATE NOT NULL,
    end_date        DATE NOT NULL,
    venue_id        INTEGER REFERENCES venues(venue_id),
    prize_pool      NUMERIC(12,2) DEFAULT 0.00 CHECK (prize_pool >= 0),
    status          VARCHAR(20) DEFAULT 'Upcoming' CHECK (status IN ('Upcoming', 'Ongoing', 'Completed', 'Cancelled')),
    organizer_id    INTEGER REFERENCES users(user_id),
    max_teams       INTEGER DEFAULT 16 CHECK (max_teams > 1),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_dates CHECK (end_date >= start_date)
);

CREATE TABLE teams (
    team_id       SERIAL PRIMARY KEY,
    team_name     VARCHAR(100) NOT NULL,
    city          VARCHAR(100),
    coach_name    VARCHAR(100),
    tournament_id INTEGER NOT NULL REFERENCES tournaments(tournament_id) ON DELETE CASCADE,
    wins          INTEGER DEFAULT 0 CHECK (wins >= 0),
    losses        INTEGER DEFAULT 0 CHECK (losses >= 0),
    draws         INTEGER DEFAULT 0 CHECK (draws >= 0),
    points        INTEGER DEFAULT 0,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_team_per_tournament UNIQUE (team_name, tournament_id)
);

CREATE TABLE players (
    player_id     SERIAL PRIMARY KEY,
    full_name     VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    nationality   VARCHAR(100),
    position      VARCHAR(50),
    jersey_number INTEGER CHECK (jersey_number BETWEEN 1 AND 99),
    goals_scored  INTEGER DEFAULT 0 CHECK (goals_scored >= 0),
    assists       INTEGER DEFAULT 0 CHECK (assists >= 0),
    is_active     BOOLEAN DEFAULT TRUE,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE team_players (
    team_player_id SERIAL PRIMARY KEY,
    team_id        INTEGER NOT NULL REFERENCES teams(team_id) ON DELETE CASCADE,
    player_id      INTEGER NOT NULL REFERENCES players(player_id) ON DELETE CASCADE,
    joined_date    DATE DEFAULT CURRENT_DATE,
    is_captain     BOOLEAN DEFAULT FALSE,
    CONSTRAINT unique_player_per_team UNIQUE (team_id, player_id)
);
CREATE TABLE matches (
    match_id        SERIAL PRIMARY KEY,
    tournament_id   INTEGER NOT NULL REFERENCES tournaments(tournament_id) ON DELETE CASCADE,
    home_team_id    INTEGER NOT NULL REFERENCES teams(team_id),
    away_team_id    INTEGER NOT NULL REFERENCES teams(team_id),
    venue_id        INTEGER REFERENCES venues(venue_id),
    match_date      TIMESTAMP NOT NULL,
    round_name      VARCHAR(50) DEFAULT 'Group Stage',
    status          VARCHAR(20) DEFAULT 'Scheduled' CHECK (status IN ('Scheduled', 'Live', 'Completed', 'Postponed', 'Cancelled')),
    referee_name    VARCHAR(100),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT no_self_match CHECK (home_team_id <> away_team_id)
);
CREATE TABLE match_results (
    result_id       SERIAL PRIMARY KEY,
    match_id        INTEGER NOT NULL UNIQUE REFERENCES matches(match_id) ON DELETE CASCADE,
    home_score      INTEGER NOT NULL DEFAULT 0 CHECK (home_score >= 0),
    away_score      INTEGER NOT NULL DEFAULT 0 CHECK (away_score >= 0),
    winner_team_id  INTEGER REFERENCES teams(team_id),
    is_draw         BOOLEAN DEFAULT FALSE,
    match_duration  INTEGER DEFAULT 90 CHECK (match_duration > 0), -- in minutes
    notes           TEXT,
    recorded_by     INTEGER REFERENCES users(user_id),
    recorded_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_group ON users(group_id);
CREATE INDEX idx_teams_tournament ON teams(tournament_id);
CREATE INDEX idx_matches_tournament ON matches(tournament_id);
CREATE INDEX idx_matches_date ON matches(match_date);
CREATE INDEX idx_team_players_team ON team_players(team_id);
CREATE INDEX idx_team_players_player ON team_players(player_id);
