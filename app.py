# -*- coding: utf-8 -*-
"""
Created on Tue May  1 19:14:04 2018

@author: Andreas Stöckl
modified by Stefan Höller
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import json
from operator import itemgetter
from datetime import datetime as dt

personen = json.load(open("./datasets/personenliste_en_clean.json"))
datumkompakt = json.load(open("./datasets/datumliste_en_clean.json"))

dict1 = personen
personenliste = sorted(dict1.items(), key=itemgetter(1), reverse=True)
names = list(zip(*personenliste))[0]

app = dash.Dash(__name__)
server = app.server
app.title='Who is in the News!'
app.css.append_css({"external_url": "https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css"})

app.layout = html.Div([
    html.H1(children='Who is in the News!'),
    html.Div([
            dcc.Markdown('''This site gives you some **statistics and plots** of the appearence of persons in written news articles. You can use them for research
                         or journalistic purposes about how often public persons are mentioned in news articles and how these persons are related to each other.
                         ''' ),
    ],
      ),


html.Div([
    html.Div([
            dcc.Markdown('''
### The Data

The text-data comes from articles published by *Die Tagespresse* agency on their website [dietagespresse.com](https://dietagespresse.com/).
'''),
    ], className='col-lg-4'),

    html.Div([
        dcc.Markdown('''
### The Analysis

For each article a Named Entity Extraction (NER) is conducted with a **machine learning algorithm** to detect the mentions of the persons
in the texts. This algorithm uses a model which was **pretrained on a corpus** of Google news articles for English and German. The lists of
persons in the articles are used to calculate the counts and are stored in a database.'''
        ),
    ], className='col-lg-4'),

   html.Div([
          dcc.Markdown('''
### The Plots

We show a **barchart** of the counts for the most often mentioned persons. For up to four of this persons you can plot the
**timeseries** of the counts at the same time for a time period you select. For two persons you can calculate their **relation / correlation**
as a funcion of time.'''
        ),
        ], className='col-lg-4'),

],
className='row'),

    html.Div([
            html.Div([
                    html.H2(children='''Top Persons'''),
                    html.Div([
                        html.P(children='''Choose the number of persons:'''),
                        dcc.Dropdown(
                            id='histnum',
                            options=[{'label': i, 'value': i} for i in [10,15,20,25,30,35,40]],
                            value=20
                        )
                    ], className='form-control'),

                ],
            className='col-lg-4 form-group' ),

            html.Div([
                    dcc.Graph(id='barchart')
                ],
            className='col-lg-8')
        ],
    className='row'),



    html.H2(children='''Variation over time'''),

    html.Div([


    html.Div([
            html.P(children='''Choose the timespan: '''),
            dcc.DatePickerRange(
                    id='datumrange',
                    min_date_allowed=dt(2015, 1, 1),
                    max_date_allowed=dt(2018, 11, 30),
                    initial_visible_month=dt(2018, 10, 1),
                    start_date=dt(2018, 9, 20),
                    end_date=dt(2018, 10, 31)
                    ),
            ],
    className='col-lg-4  form-group form-control'),


    html.Div([
            html.P(children='''Choose the persons: '''),
            html.Div([
                    dcc.Dropdown(
                            id='name1',
                            options=[{'label': i, 'value': i} for i in names],
                            value=names[0]
                            )
                    ],
            style={'width': '24%', 'float': 'left'}),
            html.Div([
                    dcc.Dropdown(
                            id='name2',
                            options=[{'label': i, 'value': i} for i in names],
                            value=names[1]
                            )
                    ],
            style={'width': '24%', 'float': 'left'}),
            html.Div([
                    dcc.Dropdown(
                            id='name3',
                            options=[{'label': i, 'value': i} for i in names],
                            value=names[2]
                            )
                    ],
            style={'width': '24%', 'float': 'left'}),
            html.Div([
                    dcc.Dropdown(
                            id='name4',
                            options=[{'label': i, 'value': i} for i in names],
                            value=names[3]
                            )
                ],
            style={'width': '24%', 'float': 'left'}),
        ],
        className='col-lg-8 form-group form-control')


    ],
    className='row'),


    html.Div([
            dcc.Graph(id='zeitplot')
        ],
    ),

    dcc.Markdown('''**Imprint:**  [Dr. Andreas Stöckl](http://www.stoeckl.ai/impressum/) modified by Stefan Höller''')
],  className='container')


@app.callback(
    dash.dependencies.Output('zeitplot', 'figure'),
    [dash.dependencies.Input('datumrange', 'start_date'),
     dash.dependencies.Input('datumrange', 'end_date'),
     dash.dependencies.Input('name1', 'value'),
     dash.dependencies.Input('name2', 'value'),
     dash.dependencies.Input('name3', 'value'),
     dash.dependencies.Input('name4', 'value')
     ])
def update_figure_a(startdatum,enddatum,name1,name2,name3,name4):

    dict1 = datumkompakt[name1]
    dict2 = datumkompakt[name2]
    dict3 = datumkompakt[name3]
    dict4 = datumkompakt[name4]
 
    datelist = pd.date_range(start=startdatum, end=enddatum).tolist()
    datelist = pd.to_datetime((datelist))

    y_name1 =[]
    y_name2 =[]
    y_name3 =[]
    y_name4 =[]
    for date in datelist:
        if str(date).split()[0] in dict1:
            y_name1.append(dict1[str(date).split()[0]])
        else:
            y_name1.append(0)
        if str(date).split()[0] in dict2:
            y_name2.append(dict2[str(date).split()[0]])
        else:
            y_name2.append(0)
        if str(date).split()[0] in dict3:
            y_name3.append(dict3[str(date).split()[0]])
        else:
            y_name3.append(0)
        if str(date).split()[0] in dict4:
            y_name4.append(dict4[str(date).split()[0]])
        else:
            y_name4.append(0)

    trace1 = go.Scatter(
    x = datelist,
    y = y_name1,
    mode = 'lines',
    name = name1
    )
    trace2 = go.Scatter(
    x = datelist,
    y = y_name2,
    mode = 'lines',
    name = name2
    )
    trace3 = go.Scatter(
    x = datelist,
    y = y_name3,
    mode = 'lines',
    name = name3
    )
    trace4 = go.Scatter(
    x = datelist,
    y = y_name4,
    mode = 'lines',
    name = name4
    )


    return {
        'data': [trace1,trace2,trace3,trace4],
        'layout': go.Layout(
            xaxis={'title': 'Date'},
            yaxis={'title': 'Counts'},
            legend={'x': 0, 'y': 1},
            height=700,
            title='Counts over time'
        )
    }

@app.callback(
    dash.dependencies.Output('barchart', 'figure'),
    [
     dash.dependencies.Input('histnum', 'value')
     ])

def update_figure_b(histnum):
    dict1 = personen

    personenliste = sorted(dict1.items(), key=itemgetter(1),reverse=True)

    names = list(zip(*personenliste))[0][0:histnum]
    values = list(zip(*personenliste))[1][0:histnum]

    trace1 = go.Bar(
    y = names,
    x = values,
    orientation = 'h'
    )


    return {
        'data': [trace1],
        'layout': go.Layout(
            xaxis={'title': 'Counts'},
            yaxis={'autorange':'reversed'},
            height=25*histnum,
            title='Counts per person',
            margin=go.Margin(
                    l=150,
                    r=50,
                    b=50,
                    t=50,
                    pad=4
            ),

        )
    }



if __name__ == '__main__':
    app.run_server()
