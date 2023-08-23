# Changelog

A semi-comprehensive list of changes for the 2024 season!

- District participation is now recorded on TeamYear objects instead of Team objects. This impacts teams that have competed in multiple districts and simplifies pulling data from TBA.
- The Team and TeamYear offseason column was previously based on team number. Now it is based on if a team competed in at least one official event that year.
- Remove extra summary statistics (max, 95th percentile, median, mean, and standard deviation) from Year objects for total, auto, teleop, endgame, and RP EPAs.
- Convert team number from int to string in database to better support offseason teams.
- Create a new Alliance object to improve querying match results.
- Add week column to Match and TeamMatch objects, removing the need to join with the Events table to filter by week.
- Refactor the TBA sync process to check for new events and team events more frequently. More consistently use ETags to reduce unnecessary data transfer.
- Add official_winner column to Match and Alliance objects to handle tiebreakers and 2015 correctly.
- Standardize vocabulary. Replace "draw" with "tie", "qual(s)/elim(s)/playoff" with "qual/elim", "fouls/no_fouls" with "foul/no_foul"
