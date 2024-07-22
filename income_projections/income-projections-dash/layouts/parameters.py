from dash import html 
import dash_bootstrap_components as dbc

def create_year_parameters(year, user_base=False):
    parameters = [
        html.H3(f"Year {year} Parameters"),
        html.H5("General Parameters"),
        dbc.Row(
            [
                dbc.Col(html.Label("User Base" if user_base else "Growth (%)")),
                dbc.Col(
                    dbc.Input(
                        id=(
                            f"year{year}_user_base"
                            if user_base
                            else f"year{year}_growth"
                        ),
                        type="number",
                        value=1000 if user_base else 10,
                        min=0,
                    )
                ),
            ],
            className="mb-3",
        ),
        html.H5("Subscription Revenue Parameters"),
        dbc.Row(
            [
                dbc.Col(html.Label("Basic Free Tier (%)")),
                dbc.Col(
                    dbc.Input(
                        id=f"basic_tier{year}",
                        type="number",
                        value=85,
                        min=0,
                        max=100,
                        step=0.01,
                    )
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(html.Label("Curious Tier (%)")),
                dbc.Col(
                    dbc.Input(
                        id=f"curious_tier{year}",
                        type="number",
                        value=10,
                        min=0,
                        max=100,
                        step=0.01,
                    )
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(html.Label("Oracle Tier (%)")),
                dbc.Col(
                    dbc.Input(
                        id=f"oracle_tier{year}",
                        type="number",
                        value=5,
                        min=0,
                        max=100,
                        step=0.01,
                    )
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(html.Label("Total (%)")),
                dbc.Col(
                    dbc.Input(
                        id=f"total_percent_{year}",
                        type="number",
                        value=100,
                        readonly=True,
                    )
                ),
            ],
            className="mb-3",
        ),
        html.H5("Ad Revenue Parameters"),
        dbc.Row(
            [
                dbc.Col(html.Label("CPC (€/click)")),
                dbc.Col(dbc.Input(id=f"cpc{year}", type="number", value=0.5, min=0)),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(html.Label("CPM (€/1000 impressions)")),
                dbc.Col(dbc.Input(id=f"cpm{year}", type="number", value=5, min=0)),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(html.Label("CTR (%)")),
                dbc.Col(dbc.Input(id=f"ctr{year}", type="number", value=1, min=0)),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(html.Label("ARPU (€/user/month)")),
                dbc.Col(dbc.Input(id=f"arpu{year}", type="number", value=0.75, min=0)),
            ],
            className="mb-3",
        ),
    ]
    return parameters


def create_metric_explanation():
    explanations = [
        html.H3("Metric Explanations"),
        html.P("User Base: Number of users in the first year."),
        html.P("Growth (%): Year-over-year growth percentage."),
        html.P("Basic Free Tier (%): Percentage of users in the Basic Free tier."),
        html.P(
            "Curious Tier (%): Percentage of users in the Curious tier (4.99 €/month)."
        ),
        html.P(
            "Oracle Tier (%): Percentage of users in the Oracle tier (14.99 €/month)."
        ),
        html.P("CPC (€/click): Cost Per Click for ads."),
        html.P("CPM (€/1000 impressions): Cost Per Thousand Impressions for ads."),
        html.P("CTR (%): Click-Through Rate for ads."),
        html.P("ARPU (€/user/month): Average Revenue Per User per month."),
    ]
    return explanations
