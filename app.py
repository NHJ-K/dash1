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
        month_format='MMM Do, YY',
        min_date_allowed=date(2017, 1, 1),
        max_date_allowed=date(2020, 7, 10),
        initial_visible_month=date(2020, 7, 10),
        date=date(2020, 6, 5)
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
    Input('date-picker', 'date')
)
def update_figure(time_slider,date_picker):
    #print(date_picker)
    rn1 = time_slider[0]
    rn2 = time_slider[1]
    if date_picker is not None:
        date_object = date.fromisoformat(date_picker)
        print(date_object)
        date_string = date_object.strftime("%-m/%-d/%Y")  
    date_string = date_string.replace(',','/')
    date_string = date_string.replace(" ","")
    rng1 = str(date_string)+ ' ' + str(rn1)+ ":00"
    print(rng1)
    rng2 =str(date_string)+ ' ' + str(rn2) + ":00"
    print(rng2)
    dff = df[(rng1 <= df['time']) & (df['time'] <= rng2)]
    print(dff)
    fig = px.bar(x=dff['time'], y=dff['renewablespercentage'])
    fig.update_xaxes(type='category')
    fig.update_layout()
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)