import pymysql
from sqlalchemy import create_engine

import prep_data
import constants

start_year = 2002
end_year = 2002

team_matches, team_events, team_years, teams, events, years = prep_data.get_data(start_year, end_year)
engine = create_engine('mysql+pymysql://'+constants.CLOUDSQL_USER+':'+constants.CLOUDSQL_PASSWORD
    +'@'+constants.CLOUDSQL_HOST+':'+constants.CLOUDSQL_PORT+'/'+constants.CLOUDSQL_DATABASE)

team_matches.to_sql('rankings_teammatch', engine, if_exists='replace', index=False)
team_events.to_sql('rankings_teamevent', engine, if_exists='replace', index=False)
team_years.to_sql('rankings_teamyear', engine, if_exists='replace', index=False)
teams.to_sql('rankings_team', engine, if_exists='replace', index=False)
events.to_sql('rankings_event', engine, if_exists='replace', index=False)
years.to_sql('rankings_year', engine, if_exists='replace', index=False)
