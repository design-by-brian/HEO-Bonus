from skyfield.api import EarthSatellite, load, wgs84
import plotly.express as px
import pandas as pd

def _dms_to_dd(dms):
    return dms[0] + dms[1]/60 + dms[2]/3600

tles = []
with open('ISS-tle-dec.txt',"r") as f:
    lines = iter(f.readlines())
    [tles.append((s,t)) for s, t in zip(lines, lines)]

positions = {'name': [], 'lat': [], 'lon': [], 'datetime': []}

ts = load.timescale()
satellite = EarthSatellite(tles[0][0], tles[0][1], 'ISS', ts)
t= ts.utc(2000,1,1)
for minute in range(0, 100):
    if minute < 60:
        t = ts.utc(2023, 12, 1, 0, minute, 0)
        positions['datetime'].append('2023-12-01T00:{}:03Z'.format(minute))
    else:
        t = ts.utc(2023, 12, 1, 1, minute-60, 0)
        positions['datetime'].append('2023-12-01T01:{}:03Z'.format(minute-60))
    
    geocentric = satellite.at(t)
    lat, lon = wgs84.latlon_of(geocentric)
    lonDD = _dms_to_dd(lon.dms())
    latDD = _dms_to_dd(lat.dms())
    positions['name'].append('ISS')
    positions['lat'].append(latDD)
    positions['lon'].append(lonDD)
    
    

positions = pd.DataFrame(positions)

fig = px.scatter_geo(positions,
                    lat=positions['lat'],
                    lon=positions['lon'],
                    hover_name="name",
                    hover_data="datetime",
                    animation_frame="datetime",
                    )
fig.add_scattergeo(name='Orbital Path',
                    lat=positions['lat'],
                    lon=positions['lon'],
                    mode='lines',
                    opacity=0.5)

fig.show()