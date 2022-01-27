import dash
from dash import dcc,html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_json('test.json')

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.RangeSlider(
        id='time-slider',
        min=0,
        max=24,
        value=[0, 24],
        tooltip={"placement": "bottom", "always_visible": True}
)
])

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('time-slider', 'value'))
def update_figure(time_slider):
    rn1 = time_slider[0]
    rn2 = time_slider[1]
    if rn1 < 10:
        rn1 = '0' + str(rn1)
    if rn2 < 10:
        rn2 = '0' + str(rn2)
    rng1 = "2022-01-15 " +str(rn1)+ ":00:00"
    rng2 = "2022-01-15 " + str(rn2) + ":00:00"

    dff = df[(rng1 <= df['time']) & (df['time'] <= rng2)]
  
    fig = px.bar(x=dff['time'], y=dff['forecast'])

    fig.update_layout()

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)