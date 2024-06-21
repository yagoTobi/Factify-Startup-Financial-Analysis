# Import necessary libraries
import dash
from dash import html, dcc 
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
from plotly.subplots import make_subplots

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define layout
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="revenue_chart"),
                    width=12,
                ),
            ],
            style={"height": "50%"}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3("Year 1 Parameters"),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("User Base")),
                                dbc.Col(dbc.Input(id="year1_user_base", type="number", value=1000, min=0)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("Basic Free Tier (%)")),
                                dbc.Col(dbc.Input(id="basic_tier1", type="number", value=85, min=0, max=100)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("Curious Tier (%)")),
                                dbc.Col(dbc.Input(id="curious_tier1", type="number", value=10, min=2, max=15)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("Oracle Tier (%)")),
                                dbc.Col(dbc.Input(id="oracle_tier1", type="number", value=5, min=2, max=15)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("CPC (€/click)")),
                                dbc.Col(dbc.Input(id="cpc1", type="number", value=0.5, min=0)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("CPM (€/1000 impressions)")),
                                dbc.Col(dbc.Input(id="cpm1", type="number", value=5, min=0)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("CTR (%)")),
                                dbc.Col(dbc.Input(id="ctr1", type="number", value=1, min=0)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("ARPU (€/user/month)")),
                                dbc.Col(dbc.Input(id="arpu1", type="number", value=0.75, min=0)),
                            ],
                            className="mb-3",
                        ),
                    ],
                    width=2,
                ),
                dbc.Col(
                    [
                        html.H3("Year 2 Parameters"),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("Growth (%)")),
                                dbc.Col(dbc.Input(id="year2_growth", type="number", value=10, min=0)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("Basic Free Tier (%)")),
                                dbc.Col(dbc.Input(id="basic_tier2", type="number", value=85, min=0, max=100)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("Curious Tier (%)")),
                                dbc.Col(dbc.Input(id="curious_tier2", type="number", value=10, min=2, max=15)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("Oracle Tier (%)")),
                                dbc.Col(dbc.Input(id="oracle_tier2", type="number", value=5, min=2, max=15)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("CPC (€/click)")),
                                dbc.Col(dbc.Input(id="cpc2", type="number", value=0.5, min=0)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("CPM (€/1000 impressions)")),
                                dbc.Col(dbc.Input(id="cpm2", type="number", value=5, min=0)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("CTR (%)")),
                                dbc.Col(dbc.Input(id="ctr2", type="number", value=1, min=0)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("ARPU (€/user/month)")),
                                dbc.Col(dbc.Input(id="arpu2", type="number", value=0.75, min=0)),
                            ],
                            className="mb-3",
                        ),
                    ],
                    width=2,
                ),
                # Repeat similar structure for Year 3 to Year 5
                dbc.Col(
                    [
                        html.H3("Year 3 Parameters"),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("Growth (%)")),
                                dbc.Col(dbc.Input(id="year3_growth", type="number", value=10, min=0)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("Basic Free Tier (%)")),
                                dbc.Col(dbc.Input(id="basic_tier3", type="number", value=85, min=0, max=100)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("Curious Tier (%)")),
                                dbc.Col(dbc.Input(id="curious_tier3", type="number", value=10, min=2, max=15)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("Oracle Tier (%)")),
                                dbc.Col(dbc.Input(id="oracle_tier3", type="number", value=5, min=2, max=15)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("CPC (€/click)")),
                                dbc.Col(dbc.Input(id="cpc3", type="number", value=0.5, min=0)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("CPM (€/1000 impressions)")),
                                dbc.Col(dbc.Input(id="cpm3", type="number", value=5, min=0)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("CTR (%)")),
                                dbc.Col(dbc.Input(id="ctr3", type="number", value=1, min=0)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("ARPU (€/user/month)")),
                                dbc.Col(dbc.Input(id="arpu3", type="number", value=0.75, min=0)),
                            ],
                            className="mb-3",
                        ),
                    ],
                    width=2,
                ),
                dbc.Col(
                    [
                        html.H3("Year 4 Parameters"),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("Growth (%)")),
                                dbc.Col(dbc.Input(id="year4_growth", type="number", value=10, min=0)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("Basic Free Tier (%)")),
                                dbc.Col(dbc.Input(id="basic_tier4", type="number", value=85, min=0, max=100)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("Curious Tier (%)")),
                                dbc.Col(dbc.Input(id="curious_tier4", type="number", value=10, min=2, max=15)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("Oracle Tier (%)")),
                                dbc.Col(dbc.Input(id="oracle_tier4", type="number", value=5, min=2, max=15)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("CPC (€/click)")),
                                dbc.Col(dbc.Input(id="cpc4", type="number", value=0.5, min=0)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("CPM (€/1000 impressions)")),
                                dbc.Col(dbc.Input(id="cpm4", type="number", value=5, min=0)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("CTR (%)")),
                                dbc.Col(dbc.Input(id="ctr4", type="number", value=1, min=0)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("ARPU (€/user/month)")),
                                dbc.Col(dbc.Input(id="arpu4", type="number", value=0.75, min=0)),
                            ],
                            className="mb-3",
                        ),
                    ],
                    width=2,
                ),
                dbc.Col(
                    [
                        html.H3("Year 5 Parameters"),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("Growth (%)")),
                                dbc.Col(dbc.Input(id="year5_growth", type="number", value=10, min=0)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("Basic Free Tier (%)")),
                                dbc.Col(dbc.Input(id="basic_tier5", type="number", value=85, min=0, max=100)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("Curious Tier (%)")),
                                dbc.Col(dbc.Input(id="curious_tier5", type="number", value=10, min=2, max=15)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("Oracle Tier (%)")),
                                dbc.Col(dbc.Input(id="oracle_tier5", type="number", value=5, min=2, max=15)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("CPC (€/click)")),
                                dbc.Col(dbc.Input(id="cpc5", type="number", value=0.5, min=0)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("CPM (€/1000 impressions)")),
                                dbc.Col(dbc.Input(id="cpm5", type="number", value=5, min=0)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("CTR (%)")),
                                dbc.Col(dbc.Input(id="ctr5", type="number", value=1, min=0)),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Label("ARPU (€/user/month)")),
                                dbc.Col(dbc.Input(id="arpu5", type="number", value=0.75, min=0)),
                            ],
                            className="mb-3",
                        ),
                    ],
                    width=2,
                ),
            ],
            style={"height": "50%"}
        ),
    ],
    fluid=True,
)




# Define callback to update the chart
@app.callback(
    Output("revenue_chart", "figure"),
    [
        Input("year1_user_base", "value"),
        Input("year2_growth", "value"),
        Input("year3_growth", "value"),
        Input("year4_growth", "value"),
        Input("year5_growth", "value"),
        Input("basic_tier1", "value"),
        Input("curious_tier1", "value"),
        Input("oracle_tier1", "value"),
        Input("cpc1", "value"),
        Input("cpm1", "value"),
        Input("ctr1", "value"),
        Input("arpu1", "value"),
        Input("basic_tier2", "value"),
        Input("curious_tier2", "value"),
        Input("oracle_tier2", "value"),
        Input("cpc2", "value"),
        Input("cpm2", "value"),
        Input("ctr2", "value"),
        Input("arpu2", "value"),
        Input("basic_tier3", "value"),
        Input("curious_tier3", "value"),
        Input("oracle_tier3", "value"),
        Input("cpc3", "value"),
        Input("cpm3", "value"),
        Input("ctr3", "value"),
        Input("arpu3", "value"),
        Input("basic_tier4", "value"),
        Input("curious_tier4", "value"),
        Input("oracle_tier4", "value"),
        Input("cpc4", "value"),
        Input("cpm4", "value"),
        Input("ctr4", "value"),
        Input("arpu4", "value"),
        Input("basic_tier5", "value"),
        Input("curious_tier5", "value"),
        Input("oracle_tier5", "value"),
        Input("cpc5", "value"),
        Input("cpm5", "value"),
        Input("ctr5", "value"),
        Input("arpu5", "value"),
    ],
)
def update_chart(
    year1_user_base, year2_growth, year3_growth, year4_growth, year5_growth,
    basic_tier1, curious_tier1, oracle_tier1,
    cpc1, cpm1, ctr1, arpu1,
    basic_tier2, curious_tier2, oracle_tier2,
    cpc2, cpm2, ctr2, arpu2,
    basic_tier3, curious_tier3, oracle_tier3,
    cpc3, cpm3, ctr3, arpu3,
    basic_tier4, curious_tier4, oracle_tier4,
    cpc4, cpm4, ctr4, arpu4,
    basic_tier5, curious_tier5, oracle_tier5,
    cpc5, cpm5, ctr5, arpu5,
):
    # Calculate user base for each year
    user_base = [year1_user_base]
    growth_rates = [year2_growth, year3_growth, year4_growth, year5_growth]
    for growth in growth_rates:
        user_base.append(user_base[-1] * (1 + growth / 100))

    # Calculate subscription revenue and user distribution
    subscription_revenue = []
    basic_users = []
    curious_users = []
    oracle_users = []

    tiers = [
        (basic_tier1, curious_tier1, oracle_tier1),
        (basic_tier2, curious_tier2, oracle_tier2),
        (basic_tier3, curious_tier3, oracle_tier3),
        (basic_tier4, curious_tier4, oracle_tier4),
        (basic_tier5, curious_tier5, oracle_tier5)
    ]
    
    cpc = [cpc1, cpc2, cpc3, cpc4, cpc5]
    cpm = [cpm1, cpm2, cpm3, cpm4, cpm5]
    ctr = [ctr1, ctr2, ctr3, ctr4, ctr5]
    arpu = [arpu1, arpu2, arpu3, arpu4, arpu5]

    for i, users in enumerate(user_base):
        basic = users * (tiers[i][0] / 100)
        curious = users * (tiers[i][1] / 100) * 4.99
        oracle = users * (tiers[i][2] / 100) * 14.99
        subscription_revenue.append(curious + oracle)
        basic_users.append(basic)
        curious_users.append(users * (tiers[i][1] / 100))
        oracle_users.append(users * (tiers[i][2] / 100))

    # Calculate ad revenue
    ad_revenue = []
    for i, users in enumerate(user_base):
        impressions = users * (ctr[i] / 100) * 12 * 1000
        clicks = users * (ctr[i] / 100) * 12
        revenue = (impressions / 1000) * cpm[i] + clicks * cpc[i] + users * arpu[i] * 12
        ad_revenue.append(revenue)

    # Total revenue
    total_revenue = [sub_rev + ad_rev for sub_rev, ad_rev in zip(subscription_revenue, ad_revenue)]

    # Create stacked bar chart with line graph
    years = ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add bars for subscription tiers and ad revenue
    fig.add_trace(go.Bar(name="Basic Users", x=years, y=basic_users, text=basic_users, textposition='auto'), secondary_y=False)
    fig.add_trace(go.Bar(name="Curious Users", x=years, y=curious_users, text=curious_users, textposition='auto'), secondary_y=False)
    fig.add_trace(go.Bar(name="Oracle Users", x=years, y=oracle_users, text=oracle_users, textposition='auto'), secondary_y=False)
    fig.add_trace(go.Bar(name="Ad Revenue", x=years, y=ad_revenue, text=ad_revenue, textposition='auto'), secondary_y=False)
    
    # Add line for total revenue
    fig.add_trace(go.Scatter(name="Total Revenue", x=years, y=total_revenue, mode='lines+markers', line=dict(color='black')), secondary_y=True)

    # Add line for user base
    fig.add_trace(go.Scatter(name="Total Users", x=years, y=user_base, mode='lines+markers', line=dict(color='blue')), secondary_y=True)

    # Update layout
    fig.update_layout(
        barmode="stack",
        title="Revenue Year Over Year",
        xaxis={"title": "Year"},
        yaxis={"title": "Revenue (€)"},
        yaxis2={"title": "Total Users"},
    )

    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
