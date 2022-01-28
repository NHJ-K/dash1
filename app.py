from datetime import date
import dash
from dash import dcc,html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json

app = dash.Dash(__name__)

df = pd.read_csv('dataset.csv')
#print(df)
app.layout = html.Div([
    dcc.DatePickerSingle(
        id='date-picker',
        min_date_allowed=date(2017, 1, 1),
        max_date_allowed=date(2020, 10, 7),
        initial_visible_month=date(2020, 8, 5),
        date=date(2020, 8, 5)
    ),
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
    Input('time-slider', 'value'),
    Input('date-picker', 'value')
)
def update_figure(time_slider,date_picker):
    print(date_picker)
    if date_picker is not None:
        date_object = date.fromisoformat(date_picker)
        date_string = date_object.strftime('%B %d, %Y')
        print(string_prefix + date_string)
    rn1 = time_slider[0]
    rn2 = time_slider[1]
    if rn1 < 10:
        rn1 = '0' + str(rn1)
    if rn2 < 10:
        rn2 = '0' + str(rn2)

    rng1 = "2022-01-15 " +str(rn1)+ ":00:00"
    rng2 = "2022-01-15 " + str(rn2) + ":00:00"
    
    dff = df[(rng1 <= df['time']) & (df['time'] <= rng2)]
    #print(dff)
    fig = px.bar(x=dff['time'], y=dff['renewablespercentage'])
    fig.update_xaxes(type='category')
    fig.update_layout()
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)