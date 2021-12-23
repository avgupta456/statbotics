from db.models.event import Event, EventORM
from db.models.match import Match, MatchORM
from db.models.team import Team, TeamORM
from db.models.team_event import TeamEvent, TeamEventORM
from db.models.team_match import TeamMatch, TeamMatchORM
from db.models.team_year import TeamYear, TeamYearORM
from db.models.year import Year, YearORM
from db.write.template import update_template

update_events = update_template(EventORM, Event)
update_matches = update_template(MatchORM, Match)
update_teams = update_template(TeamORM, Team)
update_years = update_template(YearORM, Year)
update_team_events = update_template(TeamEventORM, TeamEvent)
update_team_matches = update_template(TeamMatchORM, TeamMatch)
update_team_years = update_template(TeamYearORM, TeamYear)
