
use kreupai;
CREATE VIEW match_summary AS
SELECT 
    m.match_dt,
    mr.teamid,
    mr.opponentid,
    mr.ishome,
    mr.goals_scored,
    mr.goals_conceded
FROM matchresults mr
JOIN matches m 
    ON mr.matchid = m.matchid
JOIN teamid t1 
    ON mr.teamid = t1.teamid
JOIN teamid t2 
    ON mr.opponentid = t2.teamid;


SELECT round(AVG(goals_scored),1) AS team_avg_goals_last5
FROM (
    SELECT goals_scored
    FROM match_summary
    WHERE teamid = 1799
    ORDER BY match_dt DESC
    LIMIT 5
) AS A;

SELECT round(AVG(goals_conceded),1) AS team_avg_conceded_last5
FROM (
    SELECT goals_conceded
    FROM match_summary
    WHERE teamid = 1799
    ORDER BY match_dt DESC
    LIMIT 5
) AS A;

SELECT round(AVG(goals_scored),1) AS team_home_goals_avg
FROM (
    SELECT goals_scored
    FROM match_summary
    WHERE teamid = 1799 and ishome=1
) AS A;

SELECT round(AVG(goals_scored),1) AS opponent_away_goals_avg
FROM (
    SELECT goals_scored
    FROM match_summary
    WHERE teamid = 53 and ishome=0
) AS A;

SELECT round(AVG(goals_conceded),1) AS opponent_avg_conceded_last5
FROM (
    SELECT goals_conceded
    FROM match_summary
    WHERE teamid = 53
    ORDER BY match_dt DESC
    LIMIT 5
) AS A;

SELECT round(AVG(goals_scored),1) AS opponent_avg_goals_last5
FROM (
    SELECT goals_scored
    FROM match_summary
    WHERE teamid = 53
    ORDER BY match_dt DESC
    LIMIT 5
) AS A;