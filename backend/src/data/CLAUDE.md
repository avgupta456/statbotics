# CLAUDE.md — `src/data/`

## Seeding EPA Means from Preseason Events

Before week 1 data exists, `avg.py` has a year-specific override block that hardcodes the component means used to seed EPA ratings. The block is skipped automatically once week 1 matches are present.

Run this single query against the DB (note: RP columns are booleans and require `::int` cast):

```sql
SELECT
    AVG((red_score + blue_score) / 2.0)           AS score_mean,
    STDDEV((red_score + blue_score) / 2.0)         AS score_sd,
    AVG((red_no_foul + blue_no_foul) / 2.0)        AS no_foul_mean,
    AVG((red_foul + blue_foul) / 2.0)              AS foul_mean,
    AVG((red_auto + blue_auto) / 2.0)              AS auto_mean,
    AVG((red_teleop + blue_teleop) / 2.0)          AS teleop_mean,
    AVG((red_endgame + blue_endgame) / 2.0)        AS endgame_mean,
    AVG((red_rp_1::int + blue_rp_1::int) / 2.0)   AS rp_1_mean,
    AVG((red_rp_2::int + blue_rp_2::int) / 2.0)   AS rp_2_mean,
    AVG((red_rp_3::int + blue_rp_3::int) / 2.0)   AS rp_3_mean,
    -- Include comp_1 through comp_N where N is the number of comps defined
    -- for that year in key_to_name[YEAR] in src/breakdown.py (max 18, varies by year)
    AVG((red_comp_1 + blue_comp_1) / 2.0)          AS comp_1_mean,
    AVG((red_comp_2 + blue_comp_2) / 2.0)          AS comp_2_mean,
    -- ... through comp_N_mean
    COUNT(*)                                        AS num_matches
FROM matches
WHERE event = '{YEAR}week0' AND status = 'Completed';
```

Set `tiebreaker_mean` based on the year's specific tiebreaker rule — it is not always `no_foul_mean`. Check `clean_breakdown_{year}()` in `src/tba/breakdown.py` to confirm what value is assigned to `tiebreaker` for that year. Add a `# TODO: Remove once week 1 data is available` comment to the override block.
