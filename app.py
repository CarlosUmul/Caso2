import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
import requests
import plotly as pl

df = pd.read_excel("unificado.xlsx")

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server=app.server

app.title="Dashboard"

cuentas = ["Inflacion", "Remesas", "Emision"]

app.layout = html.Div([
    html.Div([
        html.Div([
            # First drop-down for selecting years
            html.Div(dcc.Dropdown(
                id="inflaciondd",
                value=["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"],
                clearable=False,
                multi=True,
                options=[{'label': x, 'value': x} for x in sorted(df.Año.unique())]
            ), className="six columns", style={"width": "50%"}),

            # Second drop-down for selecting an indicator
            html.Div(dcc.Dropdown(
                id="indicador_indd",
                value="Inflacion",
                clearable=False,
                options=[{'label': x, 'value': x} for x in cuentas]
            ), className="six columns"),
        ], className="row"),
    ], className="custom-dropdown"),

    # Line chart
    html.Div([dcc.Graph(id="graph", figure={}, config={"displayModeBar": True, "displaylogo": False,})], style={'width': '1100px'}),

    # Box plot
    html.Div([dcc.Graph(id="boxplot", figure={},)], style={"width": '1100px'}),

    # Pie chart
    html.Div([dcc.Graph(id="pie", figure={},)], style={"width": '1100px'}),

    # Table
    html.Div(html.Div(id="table-container"), style={'marginBottom': '15px', 'marginTop': "10px"}),
])

@app.callback(
    [
        Output(component_id="graph", component_property="figure"),
        Output(component_id="boxplot", component_property="figure"),
        Output(component_id="pie", component_property="figure"),
        Output("table-container", 'children')],
    [
        Input(component_id="inflaciondd", component_property="value"),
        Input(component_id="indicador_indd", component_property="value")
    ]
)

def display_value(selected_company, selected_account):
    fig = px.line(df2, color="Año", x="Mes", markers=True, y=selected_account, width=1000, height=500)

    fig2 = px.box(df2, color="Año", x="Año", y=selected_account, width=1000, height=500)

    fig3 = px.pie(df2, names="Año", values=selected_account, width=1000, height=500)
    
    # Modify the data frame for the table
    df_reshaped = df2.pivot(index='Año', columns='Mes', values=selected_account)
    df_reshaped_2 = df_reshaped.reset_index()
    
    # Table
    table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df_reshaped_2.columns],
        data=df_reshaped_2.to_dict("records"),
        export_format="csv",
        style_table={'width': '100%'},
        style_header={'backgroundColor': 'blue', 'color': 'white', 'fontWeight': 'bold'}
    )

    return fig, fig2, fig3, table

# Set the server and run it
if __name__ == '__main__':
    app.run_server(debug=False,host="0.0.0.0",port=10000)
