#AUTHOR: BRIAN SMITH
#DATE:27/01/2023

from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from orbit import get_orbit, plot_earth
import pandas as pd
import dash

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "24rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}


sidebar = html.Div(
    [
        html.H2("Filters"),
        html.Hr(),
        html.P(
            "Select a station and month...", className="lead"
        ),
        dbc.Nav(
            [
                dcc.Dropdown(options=['Chinese Space Station - CSS', 'International Space Station - ISS'], 
                             value='Chinese Space Station - CSS', id = 'station-selection'),
                html.Br(),
                dcc.Dropdown(options=['November 2023', 'December 2023', 'January 2024'], 
                             value='January 2024', id='date-selection'),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),
        html.P(
            "Earth not to scale."
        )
    ],
    style=SIDEBAR_STYLE,
)

tle_list = []

with open('CSS-tle-nov.txt',"r") as f:
    dict = {'Station': 'Chinese Space Station - CSS',
            'Month': 'November 2023',
            'TLE': f.readlines()}
    tle_list.append(dict)

with open('ISS-tle-nov.txt',"r") as f:
    dict = {'Station': 'International Space Station - ISS',
            'Month': 'November 2023',
            'TLE': f.readlines()}
    tle_list.append(dict)

with open('CSS-tle-dec.txt',"r") as f:
    dict = {'Station': 'Chinese Space Station - CSS',
            'Month': 'December 2023',
            'TLE': f.readlines()}
    tle_list.append(dict)

with open('ISS-tle-dec.txt', "r") as f:
    dict = {'Station': 'International Space Station - ISS',
            'Month': 'December 2023',
            'TLE': f.readlines()}
    tle_list.append(dict)

with open('CSS-tle-jan.txt',"r") as f:
    dict = {'Station': 'Chinese Space Station - CSS',
            'Month': 'January 2024',
            'TLE': f.readlines()}
    tle_list.append(dict)

with open('ISS-tle-jan.txt', "r") as f:
    dict = {'Station': 'International Space Station - ISS',
            'Month': 'January 2024',
            'TLE': f.readlines()}
    tle_list.append(dict)

tle_df = pd.DataFrame(tle_list)

app = dash.Dash(external_stylesheets=[dbc.themes.LUX])
server = app.server

app.layout = html.Div(children = [
                dbc.Row([
                    dbc.Col(),

                    dbc.Col(html.H1('CSS and ISS Historical Orbits (ECEF)'),width = 9, style = {'margin-left':'7px','margin-top':'7px'})
                    ]),
                dbc.Row(
                    [dbc.Col(sidebar),
                    dbc.Col(dcc.Graph(id='graph-content'), width = 9, style = {'margin-left':'15px', 'margin-top':'7px', 'margin-right':'15px'})
                    ])
    ]
)

@app.callback(
    Output('graph-content', 'figure'),
    Input('station-selection', 'value'),
    Input('date-selection', 'value')
)
def update_graph(station, month):
    df_row = tle_df.loc[(tle_df['Station']==station) & (tle_df['Month']==month)]
    orbit_data = get_orbit(df_row['TLE'].values[0])
    fig = px.line_3d(orbit_data, x="x", y="y", z="z", width=850, height=850, labels={'x': 'x (km)', 'y': 'y (km)', 'z': 'z (km)'})
    plot_earth(fig=fig)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)