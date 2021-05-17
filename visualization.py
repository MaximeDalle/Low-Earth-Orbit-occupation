import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from copy import deepcopy

# Import et prepare data
data = pd.read_csv('data.csv', sep = ',')

data['size'] = [10 if name == 'ISS (ZARYA)'
               else 5
               for name in data['name']]

data['color']  = [
                    'blue'
                    if 'STARLINK' in name
                    else 'green' if 'FLOCK' in name
                    else 'red' if name == 'ISS (ZARYA)'
                    else 'purple'
                    for name in data['name']]

data['color_operator'] = [
                    'icons/blue.png'
                    if 'STARLINK' in name
                    else 'icons/red.png' if 'FLOCK' in name
                    else 'icons/black.png'
                    for name in data['name']]

data['color_operator_label'] = [
                    'SpaceX - STARLINK'
                    if 'STARLINK' in name
                    else 'Planet Labs - FLOCK' if 'FLOCK' in name
                    else 'ISS' if name == 'ISS (ZARYA)'
                    else 'Other objects'
                    for name in data['name']]

data['coords'] = data['coords'].apply(lambda x: eval(x))
data['lat'] = data['coords'].apply(lambda x: x[1])
data['lon'] = data['coords'].apply(lambda x: x[0])
data['alt'] = data['coords'].apply(lambda x: round(x[2]))

data['color_alt'] = [
                    'icons/yellow.png'
                    if alt <= 500
                    else 'icons/orange.png' if alt <= 600
                    else 'icons/red.png'
                    for alt in data['alt']]

# Initialize figure with subplots
fig = make_subplots(
    rows=1, cols=2,
    column_widths=[0.7, 0.3],
    specs=[[{"type": "scattergeo"}, {"type": "bar"}]])

# Add scattergeo globe map for objects types
fig.add_trace(
    go.Scattergeo(lat = data["lat"],
                  lon = data["lon"],
                  mode = "markers",
                  customdata = data,
                  hovertemplate = "%{customdata[1]}<br>Altitude : %{customdata[26]} km<extra></extra>",
                  showlegend = False,
                  marker = dict(color=data['color'], size=data['size'])),
    row = 1, col = 1
)

# Add histogram with the altitude
hist = px.strip(
    data,
    y = 'alt',
    color = 'color_operator_label',
    custom_data = ['name'])

hist.data[0].showlegend = False
hist.data[0].hovertemplate = "%{customdata[0]}<br>Altitude : %{y} km<extra></extra>"
hist.data[1].hovertemplate = "%{customdata[0]}<br>Altitude : %{y} km<extra></extra>"
hist.data[2].hovertemplate = "%{customdata[0]}<br>Altitude : %{y} km<extra></extra>"
hist.data[3].hovertemplate = "%{customdata[0]}<br>Altitude : %{y} km<extra></extra>"

hist.data[0].marker.color = 'purple'
hist.data[1].marker.color = 'red'
hist.data[2].marker.color = 'green'
hist.data[3].marker.color = 'blue'

hist.layout.yaxis.title.text = "Altitude (km)"

fig.add_trace(hist.data[0], row = 1, col = 2)
fig.add_trace(hist.data[3], row = 1, col = 2)
fig.add_trace(hist.data[2], row = 1, col = 2)
fig.add_trace(hist.data[1], row = 1, col = 2)

fig.layout.yaxis.title.text = "Altitude (km)"
fig.layout.yaxis.domain = [0,1]

# Update geo subplot properties
fig.update_geos(
    projection_type="orthographic",
    landcolor="burlywood",
    oceancolor="LightBlue",
    showocean=True,
    lakecolor="LightBlue"
)
# Set theme, margin, and annotation in layout
fig.update_layout(
    template="plotly_dark",
    margin=dict(r=20, t=60, b=20, l=20),
    annotations=[
        dict(
            text="Source:<br>Celestrak/NORAD/NASA",
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=0)
    ]
)

fig.layout.title = {'text': 'Objects in low Earth orbit',
                    'font': {
                        'size': 24
                    },
                   'x': 0.5,
                   'y': 0.97}
fig.show()
fig.write_html("Objects.html")