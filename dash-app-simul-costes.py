import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

# Initialize the app
app = dash.Dash(__name__)
server = app.server

# Define the initial layout
app.layout = html.Div(
    style={
        "backgroundColor": "#001f3f",
        "height": "100vh",
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "center",
        "fontFamily": "Arial, sans-serif" 
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
                "fontFamily": "Arial, sans-serif" 
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
                        html.Label("Salarios Medios por Rol (€)"),
                        html.Label("Full Stack Developer"),
                        dcc.Input(
                            id="full_stack_developer_salary",
                            type="number",
                            value=27125,
                            style={"marginBottom": "20px", "width": "100%"},
                        ),
                        html.Label("AI Researcher"),
                        dcc.Input(
                            id="ai_researcher_salary",
                            type="number",
                            value=52500,
                            style={"marginBottom": "20px", "width": "100%"},
                        ),
                        html.Label("Cloud Developer"),
                        dcc.Input(
                            id="cloud_developer_salary",
                            type="number",
                            value=37500,
                            style={"marginBottom": "20px", "width": "100%"},
                        ),
                        html.Label("Journalist"),
                        dcc.Input(
                            id="journalist_salary",
                            type="number",
                            value=21000,
                            style={"marginBottom": "20px", "width": "100%"},
                        ),
                        html.Label("Marketing Sales"),
                        dcc.Input(
                            id="marketing_sales_salary",
                            type="number",
                            value=30000,
                            style={"marginBottom": "20px", "width": "100%"},
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
        Input("full_stack_developer_salary", "value"),
        Input("ai_researcher_salary", "value"),
        Input("cloud_developer_salary", "value"),
        Input("journalist_salary", "value"),
        Input("marketing_sales_salary", "value"),
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
    full_stack_developer_salary,
    ai_researcher_salary,
    cloud_developer_salary,
    journalist_salary,
    marketing_sales_salary,
    show_bars,
):
    # Update the ratios
    ratio = {
        "engineers": engineer_ratio,
        "journalists": journalist_ratio,
        "sales_marketing": marketing_ratio,
    }

    # Function to calculate the number of employees in each category
    def calculate_employee_numbers(num_employees):
        num_engineers = (num_employees * ratio["engineers"]) // sum(ratio.values())
        num_journalists = (num_employees * ratio["journalists"]) // sum(ratio.values())
        num_sales_marketing = (num_employees * ratio["sales_marketing"]) // sum(
            ratio.values()
        )
        return num_engineers, num_journalists, num_sales_marketing

    # Define the salaries and costs based on the provided data
    salaries = {
        "full_stack_developer": full_stack_developer_salary,
        "ai_researcher": ai_researcher_salary,
        "cloud_developer": cloud_developer_salary,
        "journalist": journalist_salary,
        "marketing_sales": marketing_sales_salary,
    }

    social_security_rate = 0.236

    # Initialize lists to store the data for the graph
    years = []
    engineer_costs = []
    journalist_costs = []
    marketing_costs = []
    social_security_costs = []
    total_costs = []

    # Initialize lists to store the number of employees for the annotations
    engineer_numbers = []
    journalist_numbers = []
    marketing_numbers = []

    # Simulate the hiring process over the years
    num_employees = 2
    year = 1

    while num_employees <= max_employees:
        years.append(year)

        # Calculate the number of employees in each department based on the ratio
        num_engineers, num_journalists, num_sales_marketing = (
            calculate_employee_numbers(num_employees)
        )

        # Calculate department costs
        engineer_cost = (
            (num_engineers // 3) * salaries["full_stack_developer"]
            + (num_engineers // 3) * salaries["ai_researcher"]
            + (num_engineers // 3) * salaries["cloud_developer"]
        )
        journalist_cost = num_journalists * salaries["journalist"]
        marketing_cost = num_sales_marketing * salaries["marketing_sales"]

        total_salaries = engineer_cost + journalist_cost + marketing_cost
        social_security_cost = total_salaries * social_security_rate
        total_cost = total_salaries + social_security_cost

        if total_cost > yearly_budget or num_employees > max_employees:
            break

        engineer_costs.append(engineer_cost)
        journalist_costs.append(journalist_cost)
        marketing_costs.append(marketing_cost)
        social_security_costs.append(social_security_cost)
        total_costs.append(total_cost)

        # Store the number of employees for the annotations
        engineer_numbers.append(num_engineers)
        journalist_numbers.append(num_journalists)
        marketing_numbers.append(num_sales_marketing)

        # Increment the number of employees and year
        num_employees += max_hires_per_year
        year += 1

    # Create traces for each department
    fig = go.Figure()

    if "mostrar" in show_bars:
        fig.add_trace(
            go.Bar(
                x=years,
                y=engineer_costs,
                name="Engineering",
                text=engineer_numbers,
                textposition="auto",
            )
        )

        fig.add_trace(
            go.Bar(
                x=years,
                y=journalist_costs,
                name="Journalism",
                base=engineer_costs,
                text=journalist_numbers,
                textposition="auto",
            )
        )

        fig.add_trace(
            go.Bar(
                x=years,
                y=marketing_costs,
                name="Marketing",
                base=[i + j for i, j in zip(engineer_costs, journalist_costs)],
                text=marketing_numbers,
                textposition="auto",
            )
        )

        fig.add_trace(
            go.Bar(
                x=years,
                y=social_security_costs,
                name="Social Security",
                base=[
                    i + j + k
                    for i, j, k in zip(
                        engineer_costs, journalist_costs, marketing_costs
                    )
                ],
                text=[
                    f"{num_engineers + num_journalists + num_sales_marketing} employees"
                    for num_engineers, num_journalists, num_sales_marketing in zip(
                        engineer_numbers, journalist_numbers, marketing_numbers
                    )
                ],
                textposition="auto",
            )
        )

    # Add line trace for total costs
    fig.add_trace(
        go.Scatter(
            x=years,
            y=total_costs,
            mode="lines+markers+text",
            name="Total Cost",
            line=dict(color="red", width=2),
            text=[f"€{cost:,.0f}" for cost in total_costs],
            textposition="top center",
        )
    )

    # Update layout for better readability
    fig.update_layout(
        barmode="stack",
        title="Cost Progression for Team Growth",
        xaxis_title="Year",
        yaxis_title="Cost (€)",
        legend_title="Department",
        template="plotly_white",
    )

    return fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
