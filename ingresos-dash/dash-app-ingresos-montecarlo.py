import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import io
from dash import dcc

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def monte_carlo_simulation(num_simulations):
    # Parameter distributions
    user_base_dist = np.random.uniform(50000, 100000, num_simulations)
    growth_dist = np.random.uniform(30, 50, (num_simulations, 5)) / 100
    basic_tier_dist = np.random.uniform(70, 80, (num_simulations, 5)) / 100
    curious_tier_dist = np.random.uniform(15, 20, (num_simulations, 5)) / 100
    oracle_tier_dist = np.random.uniform(5, 10, (num_simulations, 5)) / 100
    cpc_dist = np.random.uniform(0.20, 0.50, (num_simulations, 5))
    cpm_dist = np.random.uniform(2, 5, (num_simulations, 5))
    ctr_dist = np.random.uniform(0.5, 1.5, (num_simulations, 5)) / 100
    arpu_dist = np.random.uniform(0.50, 1.50, (num_simulations, 5))

    simulations = []
    for i in range(num_simulations):
        user_base_sim = [user_base_dist[i]]
        revenue_sim = []
        for j in range(5):
            user_base_sim.append(user_base_sim[-1] * (1 + growth_dist[i, j]))
            basic_users_sim = user_base_sim[-1] * basic_tier_dist[i, j]
            curious_users_sim = user_base_sim[-1] * curious_tier_dist[i, j]
            oracle_users_sim = user_base_sim[-1] * oracle_tier_dist[i, j]
            subscription_revenue_sim = (
                curious_users_sim * 4.99 + oracle_users_sim * 14.99
            )
            impressions_sim = user_base_sim[-1] * ctr_dist[i, j] * 12 * 1000
            clicks_sim = user_base_sim[-1] * ctr_dist[i, j] * 12
            ad_revenue_sim = (
                (impressions_sim / 1000) * cpm_dist[i, j]
                + clicks_sim * cpc_dist[i, j]
                + user_base_sim[-1] * arpu_dist[i, j] * 12
            )
            total_revenue_sim = subscription_revenue_sim + ad_revenue_sim
            revenue_sim.append(total_revenue_sim)
        simulations.append(revenue_sim)
    return np.array(simulations)

# Define layout
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="revenue_chart"),
                    width=9,
                ),
                dbc.Col(
                    [
                        html.H4("Monte Carlo Simulation Data", className="mb-3"),
                        html.Div(id="simulation_data_display"),
                    ],
                    width=3,
                ),
            ],
            style={"height": "50%"},
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                        "Run Monte Carlo Simulations",
                        id="btn_run_simulations",
                        color="secondary",
                    ),
                    width=2,
                )
            ]
        ),
    ],
    fluid=True,
)

@app.callback(
    [Output("revenue_chart", "figure"), Output("simulation_data_display", "children")],
    Input("btn_run_simulations", "n_clicks"),
    prevent_initial_call=True
)
def run_monte_carlo_simulations(n_clicks):
    if n_clicks is None:
        return dash.no_update

    # Number of simulations
    num_simulations = 1000

    # Run Monte Carlo Simulations
    simulations = monte_carlo_simulation(num_simulations)

    # Calculate statistics
    mean_revenue = np.mean(simulations, axis=0)
    median_revenue = np.median(simulations, axis=0)
    min_revenue = np.min(simulations, axis=0)
    max_revenue = np.max(simulations, axis=0)

    # Create figure
    years = ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(name="Mean Revenue", x=years, y=mean_revenue, text=mean_revenue, textposition='inside'), secondary_y=False)
    fig.add_trace(go.Scatter(name="Median Revenue", x=years, y=median_revenue, mode='lines+markers', line=dict(color='blue')), secondary_y=True)
    fig.add_trace(go.Scatter(name="Min Revenue", x=years, y=min_revenue, mode='lines+markers', line=dict(color='red', dash='dash')), secondary_y=True)
    fig.add_trace(go.Scatter(name="Max Revenue", x=years, y=max_revenue, mode='lines+markers', line=dict(color='green', dash='dash')), secondary_y=True)

    fig.update_layout(
        barmode="stack",
        title="Monte Carlo Simulation Results",
        xaxis={"title": "Year"},
        yaxis={"title": "Revenue (€)"},
        yaxis2={"title": "Revenue (€)"},
    )

    # Display simulation data
    simulation_data_display = dbc.Table(
        # Table Header
        [
            html.Thead(html.Tr([
                html.Th("Year"), 
                html.Th("Mean Revenue (€)"), 
                html.Th("Median Revenue (€)"), 
                html.Th("Min Revenue (€)"), 
                html.Th("Max Revenue (€)")
            ]))
        ] +
        # Table Body
        [
            html.Tbody([
                html.Tr([
                    html.Td(f"Year {i+1}"), 
                    html.Td(f"{mean_revenue[i]:,.2f}"), 
                    html.Td(f"{median_revenue[i]:,.2f}"), 
                    html.Td(f"{min_revenue[i]:,.2f}"), 
                    html.Td(f"{max_revenue[i]:,.2f}")
                ])
                for i in range(5)
            ])
        ],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True
    )


    return fig, simulation_data_display

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
