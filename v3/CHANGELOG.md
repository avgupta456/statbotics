# Changelog

A semi-comprehensive list of changes for the 2024 season!

- District participation is now recorded on TeamYear objects instead of Team objects. This impacts teams that have competed in multiple districts and simplifies pulling data from TBA.
- Remove extra summary statistics (max, 95th percentile, median, mean, and standard deviation) from Year objects for total, auto, teleop, endgame, and RP EPAs.
- Added component EPAs whose interpretation varies by year.
- Convert team number from int to string in database to better support offseason teams.
- Create a new Alliance object to improve querying match results.
- Add week column to Match objects, removing the need to join with the Events table to filter by week.
- Check for new events and new team events more frequently (every 5 minutes instead of every night).
