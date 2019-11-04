import pandas as pd

data = pd.read_csv('mlb_2016.csv')
df = data.drop(columns='Unnamed: 0')
df = df.dropna()

matches = df.shape[0]
features = df.shape[1]-1
home_wins = len(df[df.home_team_outcome == 'Win'])
home_rate = home_wins / matches *100

home_teams = df.groupby('home_team').agg({'away_team_errors':'sum','away_team_hits':'sum','away_team_runs':'sum','home_team_errors':'sum',
                                          'home_team_hits':'sum','home_team_runs':'sum','total_runs':'sum','game_hours_dec':'sum','home_team_win':'sum',
                                          'home_team_loss':'sum','attendance':'mean','temperature':'mean','wind_speed':'mean',
                                          'game_hours_dec':'mean'}).reset_index().rename({'attendance':'avg_attendance',
                                                                                          'temperature':'avg_temp','wind_speed':'avg_wind_speed',
                                                                                          'game_hours_dec':'avg_game_duration'})
away_teams = df.groupby('away_team').agg({'away_team_errors':'sum','away_team_hits':'sum','away_team_runs':'sum','home_team_errors':'sum',
                                          'home_team_hits':'sum','home_team_runs':'sum','total_runs':'sum','game_hours_dec':'sum','home_team_win':'sum',
                                          'home_team_loss':'sum','attendance':'mean','temperature':'mean','wind_speed':'mean',
                                          'game_hours_dec':'mean'}).reset_index().rename({'attendance':'avg_attendance',
                                                                                          'temperature':'avg_temp','wind_speed':'avg_wind_speed',
                                                                                          'game_hours_dec':'avg_game_duration'})


