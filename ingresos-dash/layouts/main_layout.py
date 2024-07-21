from dash import html, dcc
import dash_bootstrap_components as dbc

from .parameters import create_year_parameters, create_metric_explanation

def create_layout():
    layout = dbc.Container(
        [
            dcc.Store(
                id="tier-percentages-store", data={"basic": 85, "curious": 10, "oracle": 5}
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(id="revenue_chart"),
                        width=9,
                    ),
                    dbc.Col(
                        [
                            html.H4("Total Revenue and User Base Per Year"),
                            html.Div(id="revenue_user_display"),
                        ],
                        width=3,
                    ),
                ],
                style={"height": "50%"},
            ),
            dbc.Row(
                [
                    dbc.Col(
                        create_year_parameters(1, user_base=True),
                        width=2,
                        className="border-end",
                    ),
                    dbc.Col(create_year_parameters(2), width=2, className="border-end"),
                    dbc.Col(create_year_parameters(3), width=2, className="border-end"),
                    dbc.Col(create_year_parameters(4), width=2, className="border-end"),
                    dbc.Col(create_year_parameters(5), width=2, className="border-end"),
                    dbc.Col(create_metric_explanation(), width=2),
                ],
                style={"height": "50%"},
            ),
        ],
        fluid=True,
    )
    return layout