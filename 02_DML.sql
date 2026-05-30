INSERT INTO user_groups (group_name, description, can_manage_tournaments, can_manage_teams, can_manage_players, can_view_only) VALUES
('Admin',          'Full system access, manages all operations',        TRUE,  TRUE,  TRUE,  FALSE),
('Employee',       'Staff who manage tournaments and match data',        TRUE,  TRUE,  TRUE,  FALSE),
('Coach',          'Team coaches, can manage their own team roster',     FALSE, TRUE,  TRUE,  FALSE),
('Referee',        'Licensed referees who officiate matches',            FALSE, FALSE, FALSE, TRUE),
('Viewer',         'Read-only access for spectators and guests',         FALSE, FALSE, FALSE, TRUE);

INSERT INTO users (username, password_hash, email, full_name, group_id) VALUES
('admin',       '$2b$12$placeholder_hash_admin',   'admin@sporttdb.com',      'System Administrator',  1),
('john_emp',    '$2b$12$placeholder_hash_john',    'john@sporttdb.com',       'John Smith',            2),
('coach_ali',   '$2b$12$placeholder_hash_ali',     'ali@sporttdb.com',        'Ali Yilmaz',            3),
('referee_bob', '$2b$12$placeholder_hash_bob',     'bob@sporttdb.com',        'Bob Marley',            4),
('viewer_sue',  '$2b$12$placeholder_hash_sue',     'sue@sporttdb.com',        'Sue Chen',              5),
('coach_marta', '$2b$12$placeholder_hash_marta',   'marta@sporttdb.com',      'Marta Gomez',           3),
('emp_fatma',   '$2b$12$placeholder_hash_fatma',   'fatma@sporttdb.com',      'Fatma Kaya',            2);

INSERT INTO venues (venue_name, city, country, capacity, surface_type) VALUES
('Ataturk Olympic Stadium', 'Istanbul',   'Turkey',  76092, 'Grass'),
('Ankara Arena',            'Ankara',     'Turkey',  55000, 'Artificial Turf'),
('Izmir Sports Complex',    'Izmir',      'Turkey',  35000, 'Grass'),
('Bursa City Stadium',      'Bursa',      'Turkey',  43331, 'Grass'),
('Indoor Sports Hall A',    'Istanbul',   'Turkey',   8000, 'Indoor');

INSERT INTO tournaments (tournament_name, sport_type, start_date, end_date, venue_id, prize_pool, status, organizer_id, max_teams) VALUES
('Turkey Super Cup 2025',     'Football',   '2025-09-01', '2025-12-15', 1, 500000.00, 'Completed', 2, 16),
('Ankara Basketball League',  'Basketball', '2025-10-01', '2026-02-28', 5, 100000.00, 'Completed', 7, 8),
('Spring Football League 2026','Football',  '2026-03-15', '2026-06-30', 3,  250000.00, 'Ongoing',   2, 12),
('National Tennis Open',      'Tennis',    '2026-05-01', '2026-05-20', 5,  75000.00,  'Ongoing',   7, 32),
('Youth Volleyball Cup',      'Volleyball', '2026-06-01', '2026-06-15', 4,  30000.00,  'Upcoming',  2, 8);

INSERT INTO teams (team_name, city, coach_name, tournament_id, wins, losses, draws, points) VALUES
('Galatasaray',     'Istanbul', 'Okan Buruk',   1, 10, 2, 4, 34),
('Fenerbahce',      'Istanbul', 'Jose Mourinho', 1, 9,  3, 4, 31),
('Besiktas',        'Istanbul', 'Giovanni',     1, 7,  5, 4, 25),
('Trabzonspor',     'Trabzon',  'Abdullah Avci',1, 6,  6, 4, 22),
('Ankara Hawks',    'Ankara',   'Ali Yilmaz',   2, 14, 2, 0, 28),
('Istanbul Bulls',  'Istanbul', 'Marta Gomez',  2, 10, 6, 0, 20),
('Antalyaspor',     'Antalya',  'Coach K',      3, 5,  2, 3, 18),
('Kayserispor',     'Kayseri',  'Coach M',      3, 4,  4, 2, 14),
('Sivasspor',       'Sivas',    'Coach R',      3, 3,  4, 3, 12);

INSERT INTO players (full_name, date_of_birth, nationality, position, jersey_number, goals_scored, assists) VALUES
('Mauro Icardi',     '1993-02-19', 'Argentine', 'Forward',    9,  18, 5),
('Hakim Ziyech',     '1993-03-19', 'Moroccan',  'Midfielder', 22, 8,  12),
('Edin Dzeko',       '1986-03-17', 'Bosnian',   'Forward',    10, 14, 4),
('Dusan Tadic',      '1988-11-20', 'Serbian',   'Midfielder', 11, 6,  15),
('Rachid Ghezzal',   '1992-07-09', 'Algerian',  'Midfielder', 7,  5,  8),
('Can Bozdogan',     '2001-08-16', 'Turkish',   'Midfielder', 14, 3,  6),
('Stefano Tacchinardi','1999-01-10','Italian',  'Defender',   5,  1,  3),
('Melih Sert',       '2000-05-22', 'Turkish',   'Goalkeeper', 1,  0,  0),
('Ahmad Hassan',     '1995-11-11', 'Egyptian',  'Forward',    9,  22, 7),
('Kevin Durant',     '1988-09-29', 'American',  'Forward',    35, 0,  0);

INSERT INTO team_players (team_id, player_id, joined_date, is_captain) VALUES
(1, 1, '2024-07-01', TRUE),
(1, 2, '2024-07-01', FALSE),
(2, 3, '2024-07-01', TRUE), 
(2, 4, '2024-07-01', FALSE), 
(3, 5, '2024-07-01', FALSE), 
(3, 6, '2024-07-01', TRUE),  
(4, 7, '2024-07-01', FALSE), 
(4, 8, '2024-07-01', TRUE),  
(5, 9, '2024-09-01', TRUE),  
(6, 10,'2024-09-01', TRUE); 

INSERT INTO matches (tournament_id, home_team_id, away_team_id, venue_id, match_date, round_name, status, referee_name) VALUES
(1, 1, 2, 1, '2025-09-15 20:00:00', 'Group Stage', 'Completed', 'Bob Marley'),
(1, 3, 4, 1, '2025-09-16 18:00:00', 'Group Stage', 'Completed', 'Bob Marley'),
(1, 1, 3, 1, '2025-10-01 20:00:00', 'Group Stage', 'Completed', 'Bob Marley'),
(1, 2, 4, 2, '2025-10-02 18:00:00', 'Group Stage', 'Completed', 'Bob Marley'),
(1, 1, 4, 1, '2025-11-15 20:00:00', 'Semi Final',  'Completed', 'Bob Marley'),
(3, 7, 8, 3, '2026-03-20 18:00:00', 'Group Stage', 'Completed', 'Bob Marley'),
(3, 8, 9, 3, '2026-04-05 15:00:00', 'Group Stage', 'Completed', 'Bob Marley'),
(3, 7, 9, 3, '2026-04-20 18:00:00', 'Group Stage', 'Scheduled', 'Bob Marley');

INSERT INTO match_results (match_id, home_score, away_score, winner_team_id, is_draw, match_duration, recorded_by) VALUES
(1, 3, 1, 1, FALSE, 90, 2),
(2, 2, 2, NULL, TRUE, 90, 2),
(3, 1, 0, 1, FALSE, 90, 2),
(4, 2, 1, 2, FALSE, 90, 7),
(5, 4, 2, 1, FALSE, 90, 2),
(6, 2, 0, 7, FALSE, 90, 7),
(7, 1, 1, NULL, TRUE, 90, 7);
