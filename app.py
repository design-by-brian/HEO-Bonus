from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
from orbit import get_orbit

tle = []
with open('tianhe-tle-short.txt',"r") as f:
    tle = f.readlines()

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Historical orbits of ISS and Tiangong space stations.'),
    html.P("Select station:"),
    dcc.Dropdown(
        id="dropdown",
        options=['ISS', 'Tiangong'],
        value='ISS',
        clearable=False,
    ),
    dcc.Graph(id="graph"),
])

@app.callback(
    Output("graph", "figure"), 
    Input("dropdown", "value"))
def plot_tle(color):
    orbit_data = get_orbit(tle)
    fig = px.line_3d(orbit_data, x="x", y="y", z="z", width=800, height=800)
    return fig

app.run_server(debug=True)