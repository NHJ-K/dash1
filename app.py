from datetime import date
import dash
from dash import dcc,html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sqlite3

app = dash.Dash(__name__)

conn = sqlite3.connect('test_database') 
c = conn.cursor()

query = "CREATE TABLE IF NOT EXISTS forecasts(time TEXT,renewablespercentage TEXT,date TEXT, hour TEXT)"
c.execute(query)
conn.commit()


df = pd.read_csv('dataset.csv',usecols=['time','renewablespercentage'])
df['time'] = pd.to_datetime(df['time'])
df['date'] = df['time'].dt.date
df['hour'] = df['time'].dt.hour
df['time'] = df['time'].dt.time
c.execute("SELECT * FROM forecasts") 
df1 = pd.DataFrame(c.fetchall(),columns=['time','renewablespercentage','date','hour'])
result = pd.concat([df, df1]).drop_duplicates()
c.execute("DELETE FROM forecasts")
conn.commit()
result.to_sql('forecasts', conn, if_exists='replace', index = False)
conn.close()




df=pd.read_csv('dataset.csv')


#print(df)
app.layout = html.Div([ #main div
    html.Div( #graph blcock
        dcc.Graph(id='graph-with-slider'),style={'width': '80%'}
    ),
    html.Div([#controls block
    html.Span("Time selecter:", style={"font-weight": "bold"}),
    html.Div(#time range
        dcc.RangeSlider(
        id='time-slider',
        min=0,
        max=24,
        value=[0, 24],
        tooltip={"placement": "bottom", "always_visible": True}
        )

    ),
    html.Span("Date selecter:", style={'padding-top':'100px',"font-weight": "bold"}),
    html.Div( #date picker
        
        dcc.DatePickerSingle(
        
        id='date-picker',
        month_format='MMM Do, YY',
        min_date_allowed=date(2017, 1, 1),
        max_date_allowed=date(2020, 7, 10),
        initial_visible_month=date(2020, 7, 10),
        date=date(2020, 6, 5)
    )
    )],style={'margin-right':'10px','align-items':'center','text-align': 'center','padding-top':'150px','width':'20%'}), #controls block end
],style={ 'display': 'flex','flex-direction':'row'}) # main div end
@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('time-slider', 'value'),
    Input('date-picker', 'date')
)
def update_figure(time_slider,date_picker):

    rn1 = time_slider[0]
    rn2 = time_slider[1]
    if date_picker is not None:
        date_object = date.fromisoformat(date_picker)
        date_string =str(date_object.day)+'/'+str(date_object.month)+'/'+str(date_object.year)
    date_string = date_string.replace(',','/')
    date_string = date_string.replace(" ","")
    rng1 = str(date_string)+ ' ' + str(rn1)+ ":00"
    print(rng1)
    if rn2 == 24:
        rng2 =str(date_string)+ ' ' + str(rn2-1) + ":45"
    else:
        rng2 =str(date_string)+ ' ' + str(rn2) + ":00"
    dff=df.loc[next(iter(df[df['time']==rng1].index), 'no match'):next(iter(df[df['time']==rng2].index), 'no match')]
    fig = px.bar(x=dff['time'], y=dff['renewablespercentage'])
    fig.update_xaxes(type='category')
    fig.update_layout()
    fig.add_trace(go.Scatter(x=dff['time'],y=dff['humidity'],name='Humidity'))
    fig.add_trace(go.Scatter(x=dff['time'],y=dff['windspeed'],name='Wind Speed'))
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)