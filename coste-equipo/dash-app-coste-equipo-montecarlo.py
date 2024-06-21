import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np

# Initialize the app
app = dash.Dash(__name__)
server = app.server

# Function to perform Monte Carlo simulation for team costs
def monte_carlo_simulation(num_simulations, max_hires_per_year, max_employees, yearly_budget, salary_distributions, ratio):
    social_security_rate = 0.236
    simulations = []

    for _ in range(num_simulations):
        num_employees = 2
        year = 1
        simulation = {
            "years": [],
            "engineer_costs": [],
            "journalist_costs": [],
            "marketing_costs": [],
            "social_security_costs": [],
            "total_costs": [],
            "engineer_numbers": [],
            "journalist_numbers": [],
            "marketing_numbers": [],
        }

        while num_employees <= max_employees:
            simulation["years"].append(year)

            # Calculate the number of employees in each department based on the ratio
            num_engineers = (num_employees * ratio["engineers"]) // sum(ratio.values())
            num_journalists = (num_employees * ratio["journalists"]) // sum(ratio.values())
            num_sales_marketing = (num_employees * ratio["sales_marketing"]) // sum(ratio.values())

            # Sample salaries from distributions
            engineer_salary = np.random.uniform(*salary_distributions["full_stack_developer"])
            ai_researcher_salary = np.random.uniform(*salary_distributions["ai_researcher"])
            cloud_developer_salary = np.random.uniform(*salary_distributions["cloud_developer"])
            journalist_salary = np.random.uniform(*salary_distributions["journalist"])
            marketing_sales_salary = np.random.uniform(*salary_distributions["marketing_sales"])

            # Calculate department costs
            engineer_cost = (
                (num_engineers // 3) * engineer_salary
                + (num_engineers // 3) * ai_researcher_salary
                + (num_engineers // 3) * cloud_developer_salary
            )
            journalist_cost = num_journalists * journalist_salary
            marketing_cost = num_sales_marketing * marketing_sales_salary

            total_salaries = engineer_cost + journalist_cost + marketing_cost
            social_security_cost = total_salaries * social_security_rate
            total_cost = total_salaries + social_security_cost

            if total_cost > yearly_budget or num_employees > max_employees:
                break

            simulation["engineer_costs"].append(engineer_cost)
            simulation["journalist_costs"].append(journalist_cost)
            simulation["marketing_costs"].append(marketing_cost)
            simulation["social_security_costs"].append(social_security_cost)
            simulation["total_costs"].append(total_cost)

            # Store the number of employees for the annotations
            simulation["engineer_numbers"].append(num_engineers)
            simulation["journalist_numbers"].append(num_journalists)
            simulation["marketing_numbers"].append(num_sales_marketing)

            # Increment the number of employees and year
            num_employees += max_hires_per_year
            year += 1

        simulations.append(simulation)

    # Truncate or pad all lists to have the same length
    max_length = max(len(sim["years"]) for sim in simulations)

    for sim in simulations:
        for key in sim:
            if len(sim[key]) < max_length:
                sim[key] += [sim[key][-1]] * (max_length - len(sim[key]))
            else:
                sim[key] = sim[key][:max_length]

    return simulations

# Define the initial layout
app.layout = html.Div(
    style={
        "backgroundColor": "#001f3f",
        "height": "100vh",
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "center",
        "fontFamily": "Arial, sans-serif",
    },
    children=[
        html.H1(
            "Factify - Proyección de Coste de Personal",
            style={"color": "white", "textAlign": "center", "padding": "20px"},
        ),
        html.Div(
            style={
                "backgroundColor": "white",
                "width": "80%",
                "height": "80%",
                "display": "flex",
                "padding": "20px",
                "borderRadius": "10px",
                "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.2)",
                "color": "black",
                "fontFamily": "Arial, sans-serif",
            },
            children=[
                html.Div(
                    [
                        html.Label("Ratio - Técnicos : Periodistas : Marketing"),
                        html.Div(
                            [
                                dcc.Input(
                                    id="engineer_ratio",
                                    type="number",
                                    value=3,
                                    style={"marginRight": "5px", "width": "50px"},
                                ),
                                html.Label(":", style={"marginRight": "5px"}),
                                dcc.Input(
                                    id="journalist_ratio",
                                    type="number",
                                    value=2,
                                    style={"marginRight": "5px", "width": "50px"},
                                ),
                                html.Label(":", style={"marginRight": "5px"}),
                                dcc.Input(
                                    id="marketing_ratio",
                                    type="number",
                                    value=1,
                                    style={"width": "50px"},
                                ),
                            ],
                            style={
                                "display": "flex",
                                "alignItems": "center",
                                "marginBottom": "20px",
                            },
                        ),
                        html.Label("Max contrataciones al año"),
                        dcc.Input(
                            id="max_hires_per_year",
                            type="number",
                            value=6,
                            style={"marginBottom": "20px", "width": "100%"},
                        ),
                        html.Label("Max empleados"),
                        dcc.Input(
                            id="max_employees",
                            type="number",
                            value=250,
                            style={"marginBottom": "20px", "width": "100%"},
                        ),
                        html.Label("Presupuesto Anual para personal (€)"),
                        dcc.Input(
                            id="yearly_budget",
                            type="number",
                            value=1000000,
                            style={"marginBottom": "20px", "width": "100%"},
                        ),
                        html.Label("Mostrar gráfico de barras"),
                        dcc.Checklist(
                            id="show_bars",
                            options=[{"label": "Mostrar", "value": "mostrar"}],
                            value=["mostrar"],
                        ),
                        html.Label("Número de Simulaciones"),
                        dcc.Input(
                            id="num_simulations",
                            type="number",
                            value=1000,
                            style={"marginBottom": "20px", "width": "100%"},
                        ),
                    ],
                    style={"width": "20%", "paddingRight": "20px"},
                ),
                html.Div(
                    [dcc.Graph(id="growth_simulation_graph", style={"height": "100%"})],
                    style={"width": "80%"},
                ),
            ],
        ),
    ],
)

# Define callback to update graph based on inputs
@app.callback(
    Output("growth_simulation_graph", "figure"),
    [
        Input("engineer_ratio", "value"),
        Input("journalist_ratio", "value"),
        Input("marketing_ratio", "value"),
        Input("max_hires_per_year", "value"),
        Input("max_employees", "value"),
        Input("yearly_budget", "value"),
        Input("num_simulations", "value"),
        Input("show_bars", "value"),
    ],
)
def update_graph(
    engineer_ratio,
    journalist_ratio,
    marketing_ratio,
    max_hires_per_year,
    max_employees,
    yearly_budget,
    num_simulations,
    show_bars,
):
    # Update the ratios
    ratio = {
        "engineers": engineer_ratio,
        "journalists": journalist_ratio,
        "sales_marketing": marketing_ratio,
    }

    # Define the salary distributions based on the provided data
    salary_distributions = {
        "full_stack_developer": (22500, 27125),
        "ai_researcher": (45000, 60000),
        "cloud_developer": (30000, 45000),
        "journalist": (21000, 40500),
        "marketing_sales": (21000, 39000),
    }

    # Run Monte Carlo Simulations
    simulations = monte_carlo_simulation(num_simulations, max_hires_per_year, max_employees, yearly_budget, salary_distributions, ratio)

    # Aggregate the results
    mean_costs = {
        "engineer_costs": np.mean([sim["engineer_costs"] for sim in simulations], axis=0),
        "journalist_costs": np.mean([sim["journalist_costs"] for sim in simulations], axis=0),
        "marketing_costs": np.mean([sim["marketing_costs"] for sim in simulations], axis=0),
        "social_security_costs": np.mean([sim["social_security_costs"] for sim in simulations], axis=0),
        "total_costs": np.mean([sim["total_costs"] for sim in simulations], axis=0),
    }
    years = simulations[0]["years"]

    # Create traces for each department
    fig = go.Figure()

    if "mostrar" in show_bars:
        fig.add_trace(
            go.Bar(
                x=years,
                y=mean_costs["engineer_costs"],
                name="Engineering",
                textposition="auto",
            )
        )

        fig.add_trace(
            go.Bar(
                x=years,
                y=mean_costs["journalist_costs"],
                name="Journalism",
                base=mean_costs["engineer_costs"],
                textposition="auto",
            )
        )

        fig.add_trace(
            go.Bar(
                x=years,
                y=mean_costs["marketing_costs"],
                name="Marketing",
                base=[i + j for i, j in zip(mean_costs["engineer_costs"], mean_costs["journalist_costs"])],
                textposition="auto",
            )
        )

        fig.add_trace(
            go.Bar(
                x=years,
                y=mean_costs["social_security_costs"],
                name="Social Security",
                base=[
                    i + j + k
                    for i, j, k in zip(mean_costs["engineer_costs"], mean_costs["journalist_costs"], mean_costs["marketing_costs"])
                ],
                textposition="auto",
            )
        )

    # Add line trace for total costs
    fig.add_trace(
        go.Scatter(
            x=years,
            y=mean_costs["total_costs"],
            mode="lines+markers+text",
            name="Total Cost",
            line=dict(color="red", width=2),
            text=[f"€{cost:,.0f}" for cost in mean_costs["total_costs"]],
            textposition="top center",
        )
    )

    # Update layout for better readability
    fig.update_layout(
        barmode="stack",
        title="Cost Progression for Team Growth (Monte Carlo Simulation)",
        xaxis_title="Year",
        yaxis_title="Cost (€)",
        legend_title="Department",
        template="plotly_white",
    )

    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
