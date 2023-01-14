import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas
import json
import plotly.express as px

# Read data
with open('owid-energy-data.json', 'r') as f:
  read_data = json.load(f)


def data_by_country(countries, key):
    data_return = []
    for country in countries:
        for d in read_data[country]['data']:
            dt = {}
            if key in d.keys():
                dt['year'] = d['year']
                dt[key] = d[key]
                dt['country'] = country
                data_return.append(dt)
    return pandas.json_normalize(data_return)

def data_by_country_general(countries):
    return data_by_country(countries, 'electricity_generation')

def data_by_country_per_capita(countries):
    return data_by_country(countries, 'energy_per_capita')

def data_by_fuel(country, fuel_types):
    data_return = []
    for d in read_data[country]['data']:
        for fuel in fuel_types:
            dt = {}
            if fuel in d.keys():
                dt['year'] = d['year']
                dt[fuel] = d[fuel]
                dt['fuel_type'] = fuel
                data_return.append(dt)
    return pandas.json_normalize(data_return)


app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP])

# Selectors
year_selector1 = dcc.RangeSlider(
    id='range-slider1',
    min=1980,
    max=2022,
    marks={1980: '1980', 1990: '1990', 2000: '2000', 2010 : '2010', 2020: '2020'},
    step=1,
    value=[1980, 2022]
)

year_selector2 = dcc.RangeSlider(
    id='range-slider2',
    min=1980,
    max=2022,
    marks={1980: '1980', 1990: '1990', 2000: '2000', 2010 : '2010', 2020: '2020'},
    step=1,
    value=[1980, 2022]
)

year_selector3 = dcc.RangeSlider(
    id='range-slider3',
    min=1980,
    max=2022,
    marks={1980: '1980', 1990: '1990', 2000: '2000', 2010 : '2010', 2020: '2020'},
    step=1,
    value=[1980, 2022]
)


def country_selector_option(key_for_check):
    # This func checks if country has requested data
    options = []
    for key in read_data.keys():
        for i in read_data[key]['data']:
            if key_for_check in i.keys():
                if key not in options:
                    options.append(key)
    return options

country_selector1 = dcc.Dropdown(
    id='country_selector1',
    options=country_selector_option('electricity_generation'),
    value=['United States'],
    multi=True,
)

country_selector2 = dcc.Dropdown(
    id='country_selector2',
    options=country_selector_option('fossil_electricity'),
    value='United States',
)

country_selector3 = dcc.Dropdown(
    id='country_selector3',
    options=country_selector_option('energy_per_capita'),
    value=['United States'],
    multi=True,
)

fuel_types_options = [
    {'label': 'Total', 'value': 'electricity_generation'},
    {'label': 'Fossil fuel', 'value': 'fossil_electricity'},
    {'label': 'Biofuel', 'value': 'biofuel_electricity'},
    {'label': 'Coal', 'value': 'coal_electricity'},
    {'label': 'Gas', 'value': 'gas_electricity'},
    {'label': 'Hydro', 'value': 'hydro_electricity'},
    {'label': 'Nuclear', 'value': 'nuclear_electricity'},
    {'label': 'Oil', 'value': 'oil_electricity'},
    {'label': 'Renewable sources', 'value': 'renewables_electricity'},
    {'label': 'Solar', 'value': 'solar_electricity'},
    {'label': 'Wind', 'value': 'wind_electricity'},
]

fuel_types_selector = dcc.Dropdown(
    id='fuel_types_selector',
    options=fuel_types_options,
    value=['electricity_generation'],
    multi=True
)

# Tabs content
tab1_content = [
    dbc.Row([
        dbc.Col([
            html.P('Select period'),
            html.Div(year_selector1)
        ]),
        dbc.Col([
            html.P('Chose country'),
            html.Div(country_selector1),
        ])
    ]),
    dbc.Row(dcc.Graph(id='generation_by_country'))
]

tab2_content = [
    dbc.Row([
        dbc.Col([
            html.P('Select period'),
            html.Div(year_selector2)
        ]),
        dbc.Col([
            html.P('Chose country'),
            html.Div(country_selector2),
        ]),
        dbc.Col([
            html.P('Chose fuel type'),
            html.Div(fuel_types_selector),
        ])
    ]),
    dbc.Tabs([
        dbc.Tab(
            dbc.Row(dcc.Graph(id='generation_by_fuel')),
            label='Graph'
        ),
        dbc.Tab(
            html.Div('Table'),
            label='Tab'
        )
    ]),
]

tab3_content = [
    dbc.Row([
        dbc.Col([
            html.P('Select period'),
            html.Div(year_selector3)
        ]),
        dbc.Col([
            html.P('Chose country'),
            html.Div(country_selector3),
        ])
    ]),
    dbc.Row(dcc.Graph(id='generation_per_capita'))
]

tab4_content = [
    dbc.Row(html.H3('Thank you for checking my app!')),
    dbc.Row(html.P('Developed by Andrii Kern')),
    dbc.Row(html.P('Email: kernandrey1@gmail.com')),
    dbc.Row(html.P('Telegram: @andreykern')),
    dbc.Row(html.P("It's my first touch with Dash and I am really excited! I hope I will be a part of your team, "
                   "but anyway thanks for this task!")),
]


# Layout
app.layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                html.H2('Electricity generation dash', style={'margin-top': '20px'}),
                width={"size": 6, "offset": 3},
                style={'margin-bottom': '50px'},
            )
        ),

        dbc.Tabs([
            dbc.Tab(tab1_content, label='Electricity generation by countries', style={'margin-top': '20px'}),
            dbc.Tab(tab2_content, label='Electricity generation by source of energy', style={'margin-top': '20px'}),
            dbc.Tab(tab3_content, label='Electricity generation per capita', style={'margin-top': '20px'}),
            dbc.Tab(tab4_content, label='Contacts', style={'margin-top': '20px'})
        ])
    ],
    style={'margin-left': '50px',
           'margin-right': '50px'}
)


# Callbacks
@app.callback(
    Output(
        component_id='generation_by_country',
        component_property='figure'
    ),
    [
        Input(
            component_id='range-slider1',
            component_property='value'
        ),
        Input(
            component_id='country_selector1',
            component_property='value'
        )
    ]
)
def electricity_by_country(year, country):
    if len(country) == 0:
        return
    dt = data_by_country_general(country)
    updated_data = dt[(dt['year'] > year[0]) & (dt['year'] < year[1])]
    fig = px.line(updated_data,
                  x='year',
                  y='electricity_generation',
                  title='Electricity generation, TWh',
                  color='country')
    return fig

@app.callback(
    Output(
        component_id='generation_by_fuel',
        component_property='figure'
    ),
    [
        Input(
            component_id='range-slider2',
            component_property='value'
        ),
        Input(
            component_id='fuel_types_selector',
            component_property='value'
        ),
        Input(
            component_id='country_selector2',
            component_property='value'
        ),
    ]
)
def electricity_by_fuel(year, fuel_type, country):
    if country is None:
        return
    dt = data_by_fuel(country, fuel_type)
    updated_data = dt[(dt['year'] > year[0]) & (dt['year'] < year[1])]
    fig = px.line(updated_data,
                  x='year',
                  y=fuel_type,
                  title='Electricity generation by fuel, TWh',
                  color='fuel_type')
    return fig

@app.callback(
    Output(
        component_id='generation_per_capita',
        component_property='figure'
    ),
    [
        Input(
            component_id='range-slider3',
            component_property='value'
        ),
        Input(
            component_id='country_selector3',
            component_property='value'
        )
    ]
)
def electricity_by_country_per_capita(year, country):
    if len(country) == 0:
        return
    dt = data_by_country_per_capita(country)
    updated_data = dt[(dt['year'] > year[0]) & (dt['year'] < year[1])]
    fig = px.line(updated_data,
                  x='year',
                  y='energy_per_capita',
                  title='Electricity generation, TWh',
                  color='country')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

# Добавить в графики по странам тип вырабатываемой энергии. Добавить сравнение стран и весь мир
# Сделать то же на душу населения
# Население по странам
