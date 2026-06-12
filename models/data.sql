-- Match data for model evaluation
-- Includes all completed matches with known outcome.
--
-- Usage (CockroachDB / psql-compatible):
--   psql "postgresql://root@localhost:26257/statbotics3?sslmode=disable" \
--        -c "\copy (SELECT * FROM (<query>)) TO 'matches.csv' WITH CSV HEADER"
--
-- Or use the Python loader in runner.py which runs these directly.

-- ── matches ──────────────────────────────────────────────────────────────────
SELECT
    m.year,
    m.event,
    m.comp_level,
    m.elim,
    m.time,
    m.red_1,
    m.red_2,
    m.red_3,
    m.blue_1,
    m.blue_2,
    m.blue_3,
    m.red_score,           -- post-foul total score
    m.red_no_foul,         -- pre-foul score (NULL pre-2016)
    m.blue_score,          -- post-foul total score
    m.blue_no_foul,        -- pre-foul score (NULL pre-2016)
    m.winner
FROM matches m
WHERE m.winner   IS NOT NULL
  AND m.red_score  IS NOT NULL
  AND m.blue_score IS NOT NULL
ORDER BY m.year, m.time;

-- ── year statistics (needed for EPA normalization) ────────────────────────────
SELECT
    y.year,
    y.score_mean,
    y.score_sd,
    y.no_foul_mean
FROM years y
ORDER BY y.year;
