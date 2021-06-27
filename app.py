# -*- coding: utf-8 -*-

import colorcet
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
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
df_resources = pd.read_csv("resources.csv").drop(columns=["date"])
df_resources["link"] = "[Link](" + df_resources["link"] + ")"


options = [
    {"label": company, "value": company} for company in df_data["company"].unique()
]

app.layout = html.Div(
    children=[
        html.H1(children="Sustainability Database"),
        html.Div(
            children="""
        Choose a company to see their equivalent CO2 emissions:
    """
        ),
        dcc.Dropdown(id="company-dropdown", options=options, value=options[0]["value"]),
        dcc.Graph(
            id="bar-plot",
        ),
        dash_table.DataTable(
            id="resource-table",
            columns=[
                {"name": i, "id": i}
                for i in df_resources.drop(columns=["link"]).columns
            ]
            + [{"name": "link", "id": "link", "presentation": "markdown"}],
            sort_action="native",
            filter_action="native",
            page_action="native",
            page_size=10,
        ),
    ]
)


@app.callback(
    Output(component_id="bar-plot", component_property="figure"),
    Input(component_id="company-dropdown", component_property="value"),
)
def update_bar_plot(company):
    if company is None:
        return px.bar()
    else:
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
            showlegend=True,
            title=f"Emissions of {company}",
            xaxis=dict(tickformat="d"),
            font=dict(
                # family="Arial",
                size=12,
                color="#505050",
            ),
        )
        return fig


@app.callback(
    Output(component_id="resource-table", component_property="data"),
    Input(component_id="company-dropdown", component_property="value"),
)
def update_resource_table(company):
    if company is None:
        return df_resources.to_dict("records")
    else:
        return df_resources[df_resources["company"] == company].to_dict("records")


if __name__ == "__main__":
    app.run_server(debug=False)
