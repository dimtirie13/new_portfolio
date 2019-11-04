import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import urllib
from datetime import datetime as dt
import dash_table
import base64



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server
app.css.config.serve_locally = True



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

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': home_teams.columns, 'y': home_teams[home_teams.home_team == 'Boston Red Sox'], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)



