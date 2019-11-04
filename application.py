import dash
from flask import Flask, render_template
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash
import dash_table
import pandas as pd
import urllib
from datetime import datetime as dt
import dash_table
import pandas as pd
from data_clean_up import home_teams

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
application = Flask(__name__)






@server.route('/')
def index():
    return render_template('base.html')



app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=application, routes_pathname_prefix='/dash/')
app.css.config.serve_locally = True


app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),

        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': home_teams.home_team, 'y': home_teams.home_team_runs, 'type': 'bar', 'name': 'Home_team_runs'},
                    {'x': home_teams.home_team, 'y': home_teams.away_team_runs, 'type': 'bar', 'name': u'Away_team_runs'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        )
    ])





if __name__ == '__main__':
    app.run_server(debug=True)  



