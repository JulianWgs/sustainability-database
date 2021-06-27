# -*- coding: utf-8 -*-

import colorcet
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

template = go.layout.Template()
# 40 is usable
# (len(colorcet.kgy) - 40) // 1 - 1
template.layout["colorway"] = colorcet.kgy[80::60]

df_data = pd.read_csv("data.csv")


options = [
    {"label": company, "value": company} for company in df_data["company"].unique()
]

app.layout = html.Div(
    children=[
        html.H1(children="Hello Dash"),
        html.Div(
            children="""
        Dash: A web application framework for Python.
    """
        ),
        dcc.Dropdown(id="dropdown-company", options=options, value=options[0]["value"]),
        dcc.Graph(
            id="bar-plot",
        ),
    ]
)


@app.callback(
    Output(component_id="bar-plot", component_property="figure"),
    Input(component_id="dropdown-company", component_property="value"),
)
def update_output_div(company):
    fig = px.bar(
        df_data[df_data["company"] == company]
        .sort_values("year")
        .groupby(["company", "name", "year"])
        .last()
        .reset_index(),
        x="year",
        y="value",
        color="name",
        hover_data=["resource", "page"],
        barmode="stack",
    )
    fig.update_layout(
        template=template,
        showlegend=False,
        title=f"Emissions of {company}",
        xaxis=dict(tickformat="d"),
        font=dict(
            # family="Arial",
            size=12,
            color="#505050",
        ),
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=False)
