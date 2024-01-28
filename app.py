from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from orbit import get_orbit
import pandas as pd
import numpy as np
import dash

# Earth orbit parameters
mu = 398600.4418
r = 6500 #6781
D = 24*0.997269

uu, vv = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
xx = r * np.cos(uu) * np.sin(vv)
yy = r * np.sin(uu) * np.sin(vv)
zz = r * np.cos(vv)

tianhe_tle = []
with open('tianhe-tle.txt',"r") as f:
    tianhe_tle = f.readlines()

ISS_tle = []
with open('ISS-tle.txt', "r") as f:
    ISS_tle = f.readlines()

tle_df = pd.DataFrame({'Chinese Space Station - CSS': tianhe_tle, 'International Space Station - ISS': ISS_tle})

app = dash.Dash(external_stylesheets=[dbc.themes.LUX])
server = app.server

app.layout = html.Div([
    html.H1(children='Historical Orbits for January', style={'textAlign':'center'}),
    dcc.Dropdown(['Chinese Space Station - CSS', 'International Space Station - ISS'], 'Chinese Space Station - CSS', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])

@app.callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    orbit_data = get_orbit(tle_df[value])
    fig = px.line_3d(orbit_data, x="x", y="y", z="z", width=800, height=800)
    fig.add_surface(x=xx, y=yy, z=zz, showscale=False)
    fig.update(layout_coloraxis_showscale=False)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
