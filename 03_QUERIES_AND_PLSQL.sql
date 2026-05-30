-- QUERY 1: Tournament Standings with Team Statistics
-- (JOIN + ORDER BY + computed columns)
SELECT
    t.tournament_name,
    tm.team_name,
    tm.city,
    tm.wins,
    tm.losses,
    tm.draws,
    tm.points,
    (tm.wins + tm.losses + tm.draws) AS matches_played,
    ROUND(tm.wins::NUMERIC / NULLIF(tm.wins + tm.losses + tm.draws, 0) * 100, 1) AS win_pct
FROM teams tm
JOIN tournaments t ON tm.tournament_id = t.tournament_id
WHERE t.status IN ('Ongoing', 'Completed')
ORDER BY t.tournament_name, tm.points DESC, tm.wins DESC;

-- QUERY 2: Top Scorers Across All Tournaments
-- (JOIN through junction table + ORDER BY + LIMIT)
SELECT
    p.full_name,
    p.nationality,
    p.position,
    p.jersey_number,
    tm.team_name,
    t.tournament_name,
    t.sport_type,
    p.goals_scored,
    p.assists,
    (p.goals_scored + p.assists) AS goal_contributions
FROM players p
JOIN team_players tp ON p.player_id = tp.player_id
JOIN teams tm ON tp.team_id = tm.team_id
JOIN tournaments t ON tm.tournament_id = t.tournament_id
ORDER BY p.goals_scored DESC, p.assists DESC
LIMIT 10;

-- QUERY 3: Match Results Summary per Tournament
-- (GROUP BY + COUNT + AVG + SUM)
SELECT
    t.tournament_name,
    t.sport_type,
    COUNT(m.match_id)                        AS total_matches,
    COUNT(mr.result_id)                      AS completed_matches,
    SUM(mr.home_score + mr.away_score)       AS total_goals,
    ROUND(AVG(mr.home_score + mr.away_score), 2) AS avg_goals_per_match,
    COUNT(CASE WHEN mr.is_draw THEN 1 END)   AS draws,
    SUM(mr.home_score)                       AS home_goals,
    SUM(mr.away_score)                       AS away_goals
FROM tournaments t
JOIN matches m ON t.tournament_id = m.tournament_id
LEFT JOIN match_results mr ON m.match_id = mr.match_id
GROUP BY t.tournament_id, t.tournament_name, t.sport_type
ORDER BY total_goals DESC NULLS LAST;

-- QUERY 4: Venue Utilization Report
-- (JOIN + GROUP BY + COUNT + subquery)
SELECT
    v.venue_name,
    v.city,
    v.capacity,
    v.surface_type,
    COUNT(DISTINCT m.match_id)       AS matches_hosted,
    COUNT(DISTINCT m.tournament_id)  AS tournaments_hosted,
    (SELECT COUNT(*) FROM matches m2
     WHERE m2.venue_id = v.venue_id
     AND m2.status = 'Scheduled')   AS upcoming_matches
FROM venues v
LEFT JOIN matches m ON v.venue_id = m.venue_id
GROUP BY v.venue_id, v.venue_name, v.city, v.capacity, v.surface_type
ORDER BY matches_hosted DESC;

-- QUERY 5: User Activity & Role Report
-- (JOIN + GROUP BY + CASE)
SELECT
    ug.group_name             AS role,
    COUNT(u.user_id)          AS total_users,
    COUNT(CASE WHEN u.is_active THEN 1 END) AS active_users,
    COUNT(CASE WHEN u.last_login >= CURRENT_DATE - INTERVAL '30 days' THEN 1 END) AS active_last_30_days,
    ug.can_manage_tournaments,
    ug.can_manage_teams,
    ug.can_manage_players
FROM user_groups ug
LEFT JOIN users u ON ug.group_id = u.group_id
GROUP BY ug.group_id, ug.group_name, ug.can_manage_tournaments, ug.can_manage_teams, ug.can_manage_players
ORDER BY total_users DESC;

-- QUERY 6: Teams with Most Players (subquery + HAVING)
SELECT
    tm.team_name,
    t.tournament_name,
    t.sport_type,
    COUNT(tp.player_id) AS squad_size,
    COUNT(CASE WHEN tp.is_captain THEN 1 END) AS captains,
    STRING_AGG(p.full_name, ', ' ORDER BY tp.is_captain DESC, p.full_name) AS player_names
FROM teams tm
JOIN tournaments t ON tm.tournament_id = t.tournament_id
LEFT JOIN team_players tp ON tm.team_id = tp.team_id
LEFT JOIN players p ON tp.player_id = p.player_id
GROUP BY tm.team_id, tm.team_name, t.tournament_name, t.sport_type
HAVING COUNT(tp.player_id) > 0
ORDER BY squad_size DESC;

-- QUERY 7: Prize Pool Distribution with Winner Analysis
-- (Correlated subquery + JOIN + GROUP BY)
SELECT
    t.tournament_name,
    t.sport_type,
    t.start_date,
    t.end_date,
    t.status,
    t.prize_pool,
    t.max_teams,
    COUNT(DISTINCT tm.team_id) AS registered_teams,
    COUNT(DISTINCT m.match_id) AS total_matches,
    (SELECT tm2.team_name
     FROM teams tm2
     WHERE tm2.tournament_id = t.tournament_id
     ORDER BY tm2.points DESC
     LIMIT 1) AS current_leader,
    ROUND(t.prize_pool / NULLIF(COUNT(DISTINCT m.match_id), 0), 2) AS prize_per_match
FROM tournaments t
LEFT JOIN teams tm ON t.tournament_id = tm.tournament_id
LEFT JOIN matches m ON t.tournament_id = m.tournament_id
GROUP BY t.tournament_id, t.tournament_name, t.sport_type, t.start_date,
         t.end_date, t.status, t.prize_pool, t.max_teams
ORDER BY t.prize_pool DESC;


-- PL/SQL BLOCK 1: PROCEDURE - Record Match Result
-- Records a match score and automatically updates team standings
CREATE OR REPLACE PROCEDURE record_match_result(
    p_match_id      INTEGER,
    p_home_score    INTEGER,
    p_away_score    INTEGER,
    p_duration      INTEGER DEFAULT 90,
    p_recorded_by   INTEGER DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_home_team_id  INTEGER;
    v_away_team_id  INTEGER;
    v_winner_id     INTEGER;
    v_is_draw       BOOLEAN;
BEGIN
    SELECT home_team_id, away_team_id
    INTO v_home_team_id, v_away_team_id
    FROM matches
    WHERE match_id = p_match_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Match ID % does not exist', p_match_id;
    END IF;

    IF p_home_score > p_away_score THEN
        v_winner_id := v_home_team_id;
        v_is_draw   := FALSE;
    ELSIF p_away_score > p_home_score THEN
        v_winner_id := v_away_team_id;
        v_is_draw   := FALSE;
    ELSE
        v_winner_id := NULL;
        v_is_draw   := TRUE;
    END IF;

    INSERT INTO match_results (match_id, home_score, away_score, winner_team_id, is_draw, match_duration, recorded_by)
    VALUES (p_match_id, p_home_score, p_away_score, v_winner_id, v_is_draw, p_duration, p_recorded_by)
    ON CONFLICT (match_id) DO UPDATE
        SET home_score = p_home_score,
            away_score = p_away_score,
            winner_team_id = v_winner_id,
            is_draw = v_is_draw,
            match_duration = p_duration,
            recorded_at = CURRENT_TIMESTAMP;

    UPDATE matches SET status = 'Completed' WHERE match_id = p_match_id;

    IF v_is_draw THEN
        UPDATE teams SET draws = draws + 1, points = points + 1 WHERE team_id = v_home_team_id;
        UPDATE teams SET draws = draws + 1, points = points + 1 WHERE team_id = v_away_team_id;
    ELSIF v_winner_id = v_home_team_id THEN
        UPDATE teams SET wins = wins + 1, points = points + 3 WHERE team_id = v_home_team_id;
        UPDATE teams SET losses = losses + 1             WHERE team_id = v_away_team_id;
    ELSE
        UPDATE teams SET losses = losses + 1             WHERE team_id = v_home_team_id;
        UPDATE teams SET wins = wins + 1, points = points + 3 WHERE team_id = v_away_team_id;
    END IF;

    RAISE NOTICE 'Match % result recorded: % - %', p_match_id, p_home_score, p_away_score;
END;
$$;

CALL record_match_result(8, 2, 1, 90, 2);


-- PL/SQL BLOCK 2: FUNCTION - Get Tournament Standings
-- Returns a table of team standings for a given tournament
CREATE OR REPLACE FUNCTION get_tournament_standings(p_tournament_id INTEGER)
RETURNS TABLE (
    rank          INTEGER,
    team_name     VARCHAR,
    matches_played INTEGER,
    wins          INTEGER,
    draws         INTEGER,
    losses        INTEGER,
    goals_for     BIGINT,
    goals_against BIGINT,
    goal_diff     BIGINT,
    points        INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        ROW_NUMBER() OVER (ORDER BY tm.points DESC, tm.wins DESC)::INTEGER AS rank,
        tm.team_name,
        (tm.wins + tm.draws + tm.losses)::INTEGER AS matches_played,
        tm.wins,
        tm.draws,
        tm.losses,
        COALESCE(SUM(CASE WHEN m.home_team_id = tm.team_id THEN mr.home_score
                          WHEN m.away_team_id = tm.team_id THEN mr.away_score
                          ELSE 0 END), 0) AS goals_for,
        COALESCE(SUM(CASE WHEN m.home_team_id = tm.team_id THEN mr.away_score
                          WHEN m.away_team_id = tm.team_id THEN mr.home_score
                          ELSE 0 END), 0) AS goals_against,
        COALESCE(SUM(CASE WHEN m.home_team_id = tm.team_id THEN mr.home_score - mr.away_score
                          WHEN m.away_team_id = tm.team_id THEN mr.away_score - mr.home_score
                          ELSE 0 END), 0) AS goal_diff,
        tm.points
    FROM teams tm
    LEFT JOIN matches m ON (m.home_team_id = tm.team_id OR m.away_team_id = tm.team_id)
                        AND m.tournament_id = p_tournament_id
    LEFT JOIN match_results mr ON m.match_id = mr.match_id
    WHERE tm.tournament_id = p_tournament_id
    GROUP BY tm.team_id, tm.team_name, tm.wins, tm.draws, tm.losses, tm.points
    ORDER BY tm.points DESC, tm.wins DESC;
END;
$$;

SELECT * FROM get_tournament_standings(1);


-- PL/SQL BLOCK 3: TRIGGER - Auto-update tournament status
-- Automatically marks a tournament as 'Ongoing' or 'Completed' based on dates
CREATE OR REPLACE FUNCTION update_tournament_status()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF (SELECT COUNT(*) FROM matches
        WHERE tournament_id = (SELECT tournament_id FROM matches WHERE match_id = NEW.match_id)
        AND status != 'Completed' AND status != 'Cancelled') = 0 THEN

        UPDATE tournaments
        SET status = 'Completed'
        WHERE tournament_id = (SELECT tournament_id FROM matches WHERE match_id = NEW.match_id)
        AND status = 'Ongoing';

        RAISE NOTICE 'Tournament marked as Completed — all matches finished.';
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_update_tournament_status
AFTER INSERT OR UPDATE ON match_results
FOR EACH ROW
EXECUTE FUNCTION update_tournament_status();


-- PL/SQL BLOCK 4: FUNCTION - Player Statistics Summary
-- Returns comprehensive player statistics
CREATE OR REPLACE FUNCTION get_player_stats(p_player_id INTEGER)
RETURNS TABLE (
    player_name     VARCHAR,
    nationality     VARCHAR,
    position        VARCHAR,
    total_goals     INTEGER,
    total_assists   INTEGER,
    contributions   INTEGER,
    teams_played    BIGINT,
    tournaments     BIGINT,
    is_captain      BOOLEAN
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        p.full_name,
        p.nationality,
        p.position,
        p.goals_scored,
        p.assists,
        (p.goals_scored + p.assists) AS contributions,
        COUNT(DISTINCT tp.team_id) AS teams_played,
        COUNT(DISTINCT tm.tournament_id) AS tournaments,
        BOOL_OR(tp.is_captain) AS is_captain
    FROM players p
    LEFT JOIN team_players tp ON p.player_id = tp.player_id
    LEFT JOIN teams tm ON tp.team_id = tm.team_id
    WHERE p.player_id = p_player_id
    GROUP BY p.player_id, p.full_name, p.nationality, p.position,
             p.goals_scored, p.assists;
END;
$$;

SELECT * FROM get_player_stats(1);


-- PL/SQL BLOCK 5: PROCEDURE - Register Team to Tournament
-- Validates capacity and registers a new team
CREATE OR REPLACE PROCEDURE register_team_to_tournament(
    p_team_name     VARCHAR,
    p_city          VARCHAR,
    p_coach_name    VARCHAR,
    p_tournament_id INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_current_teams INTEGER;
    v_max_teams     INTEGER;
    v_tournament_status VARCHAR;
    v_new_team_id   INTEGER;
BEGIN
    SELECT max_teams, status INTO v_max_teams, v_tournament_status
    FROM tournaments
    WHERE tournament_id = p_tournament_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Tournament % not found', p_tournament_id;
    END IF;

    IF v_tournament_status NOT IN ('Upcoming', 'Ongoing') THEN
        RAISE EXCEPTION 'Cannot register: Tournament is %', v_tournament_status;
    END IF;

    SELECT COUNT(*) INTO v_current_teams
    FROM teams WHERE tournament_id = p_tournament_id;

    IF v_current_teams >= v_max_teams THEN
        RAISE EXCEPTION 'Tournament is full (% / % teams)', v_current_teams, v_max_teams;
    END IF;

    IF EXISTS (SELECT 1 FROM teams WHERE team_name = p_team_name AND tournament_id = p_tournament_id) THEN
        RAISE EXCEPTION 'Team "%" is already registered in this tournament', p_team_name;
    END IF;

    INSERT INTO teams (team_name, city, coach_name, tournament_id)
    VALUES (p_team_name, p_city, p_coach_name, p_tournament_id)
    RETURNING team_id INTO v_new_team_id;

    RAISE NOTICE 'Team "%" registered successfully with ID %', p_team_name, v_new_team_id;
END;
$$;

-- Usage example:
-- CALL register_team_to_tournament('New Team FC', 'Istanbul', 'Coach X', 3);
