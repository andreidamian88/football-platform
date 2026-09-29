-- FootballPlatform
-- Scout Score v0.1
-- Prototype scouting calculation

WITH player_data AS (
    SELECT
        p.first_name,
        p.last_name,
        p.position,
        c.club_name,

        EXTRACT(
            YEAR FROM AGE(CURRENT_DATE, p.date_of_birth)
        ) AS age,

        ps.goals,
        ps.assists,

        ROUND(
            (ps.goals + ps.assists) * 90.0 / ps.minutes_played,
            2
        ) AS contributions_per_90

    FROM players AS p

    JOIN clubs AS c
        ON p.club_id = c.club_id

    JOIN player_statistics AS ps
        ON p.player_id = ps.player_id
),

scored_players AS (
    SELECT
        *,

        CASE
            WHEN age <= 21 THEN 30
            WHEN age <= 23 THEN 25
            WHEN age <= 25 THEN 20
            ELSE 10
        END AS age_score,

        CASE
            WHEN goals >= 8 THEN 30
            WHEN goals >= 5 THEN 20
            WHEN goals >= 3 THEN 10
            ELSE 0
        END AS goal_score,

        CASE
            WHEN assists >= 6 THEN 25
            WHEN assists >= 4 THEN 15
            WHEN assists >= 2 THEN 10
            ELSE 0
        END AS assist_score,

        CASE
            WHEN contributions_per_90 >= 1.30 THEN 25
            WHEN contributions_per_90 >= 1.10 THEN 20
            WHEN contributions_per_90 >= 0.80 THEN 10
            ELSE 0
        END AS efficiency_score

    FROM player_data

    WHERE age <= 25
      AND contributions_per_90 >= 0.80
)

SELECT
    first_name,
    last_name,
    position,
    club_name,
    age,
    goals,
    assists,
    contributions_per_90,
    age_score,
    goal_score,
    assist_score,
    efficiency_score,

    age_score
    + goal_score
    + assist_score
    + efficiency_score AS scout_score

FROM scored_players

ORDER BY scout_score DESC;