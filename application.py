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
from data_clean_up import home_teams, away_teams, df
from baseball_scraper import batting_stats_range, pitching_stats_range

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
application = Flask(__name__)






@application.route('/')
def index():
    return render_template("index.html")

@application.route('/blog')
def blog():
    return render_template("blog.html")

@application.route('/blog/random_forest')
def rf():
    return render_template("rf.html")


app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=application, routes_pathname_prefix='/dash/')
app.css.config.serve_locally = True
app.config['suppress_callback_exceptions'] = True
batting = batting_stats_range('2019-04-01','2019-10-30')
pitching = pitching_stats_range('2019-04-01','2019-10-30')

app.layout = html.Div(children=[
        html.H1(children='MLB Dashboard'),

        html.Div(children='''
            Below is an example of a dashbaord which can handle a variaty of user inputs
        '''),
##########################################################
##                       VISUALS                       ##
##########################################################

 ############## HOME VS AWAY BAR CHART  ######################       
        html.Div([
            html.Div([
                dcc.Dropdown( 
                id='teams-dropdown',
               options=[{'label': i, 'value': i} for i in home_teams.home_team],
                value=['Miami Marlins','Boston Red Sox'],
                multi=True,
                placeholder='Select Teams...'
                
            ),

            dcc.Graph(id='teams-plot')
        ],className='six columns',style={"border":"1px black solid",'margin':'5px', 'background':'black'}),

        ############## STATS LINE GRAPH  ##################
            html.Div([
            dcc.Dropdown(
                id='team-stats-dropdown',
                options=[{'label': i, 'value': i} for i in home_teams.home_team],
                value='Miami Marlins',
                placeholder='Select a Team..'
            ),
            dcc.Graph(id='timeseries')
            ],className='six columns',style={"border":"1px black solid",'margin':'5px', 'background':'black'}),
        ],className='row'),



############### PLAYER STATS ###########################


                html.Div([
                    html.Div([
                    html.H4('Batters Stats for 2019 Season'),
                    dash_table.DataTable(
                        id='batting-table',
                        columns=[{"name": i, "id": i} for i in batting.columns],
                        data=batting.to_dict('records'),
                                        style_cell={'textAlign': 'center'},
                    style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'},
                    style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }],
                    export_format='xlsx',
                    export_headers='display',
                    filter_action="native",
                    style_table={
                                'maxHeight': '500px',
                                'overflowY': 'scroll',
                                'border': 'thin lightgrey solid',
                                
                            },
                    sort_action="native"

            )], className='six columns'),

                html.Div([
                    html.H4('Pitchers Stats for the 2019 Season'),
                    dash_table.DataTable(
                        id='pitching-table',
                        columns=[{"name": i, "id": i} for i in pitching.columns],
                        data=pitching.to_dict('records'),
                                        style_cell={'textAlign': 'center'},
                    style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'},
                    style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }],
                    export_format='xlsx',
                    export_headers='display',
                    filter_action="native",
                    style_table={
                                'maxHeight': '500px',
                                'overflowY': 'scroll',
                                'border': 'thin lightgrey solid',
                                
                            },
                    sort_action="native"

            )], className='six columns')
                ],className="row"),
        
        

############### DATA FRAME ####################

    html.Div([
        html.H3('Fixtures & Results'),
            dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict('records'),
                                    style_cell={'textAlign': 'center'},
                style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'},
                style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }],
                export_format='xlsx',
                export_headers='display',
                filter_action="native",
                style_table={
                            'maxHeight': '500px',
                            'overflowY': 'scroll',
                            'border': 'thin lightgrey solid',
                            
                        },
                sort_action="native"

        ),
        
        ]),
    ])



##########################################################
##                       CALLBACKS                      ##
##########################################################



@app.callback(
    Output(component_id='teams-plot', component_property='figure'),
    [Input(component_id='teams-dropdown', component_property='value')]
    )


def team_runs(teams):
    home_bar = home_teams[home_teams.home_team.isin(teams)]
    away_bar = away_teams[away_teams.away_team.isin(teams)]

    home_away_bar = {
            'data': [
                    {'x': home_bar.home_team, 'y': home_bar.home_team_runs, 'type': 'bar', 'name': 'Home'},
                    {'x': away_bar.away_team  , 'y': away_bar.away_team_runs, 'type': 'bar', 'name': u'Away'},
                ],
                'layout': {
                    'title': 'No. of Runs by Team at Home vs Away'
                }
            }

            
    return home_away_bar




@app.callback(
    Output(component_id='timeseries', component_property='figure'),
    [Input(component_id='team-stats-dropdown', component_property='value')]
    )

def stats_series(team):
    home_series = df[df.home_team == team].groupby('Week')['home_team_runs','home_team_errors'].sum()
    away_series = df[df.away_team == team].groupby('Week')['away_team_runs','away_team_errors'].sum()
    # runs = pd.concat([home_series, away_series.groupby(level=0).sum()], axis=1).fillna(0).reset_index()

    series = {
                'data': [
                        {'x': home_series.index, 'y': home_series.home_team_runs, 'type': 'line', 'name': u'Home Runs'},
                        {'x': home_series.index, 'y': home_series.home_team_errors, 'type': 'line', 'name': u' Home Errors'},
                        {'x': away_series.index, 'y': away_series.away_team_runs, 'type': 'line', 'name': u'Away Runs'},
                        {'x': away_series.index, 'y': away_series.away_team_errors, 'type': 'line', 'name': u' Away Errors'},
                    ],
                    'layout': {
                        'title': 'Weekly Performance'
                    }
                }
    return series

if __name__ == '__main__':
    application.run(debug=True)  



