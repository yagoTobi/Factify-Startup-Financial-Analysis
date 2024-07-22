import pandas as pd
import plotly.graph_objects as go

# Definimos los salarios anuales Españoles para los roles
salaries = {
    "full_stack_developer": 27125,
    "ai_researcher": 52500,
    "cloud_developer": 37500,
    "journalist": 21000,
    "marketing_sales": 30000,
}

# Tasa de la seguridad social definida a fecha del 2024
social_security_rate = 0.236

# Ratio de contratación estimado para la empresa 3:2:1
ratio = {"engineers": 3, "journalists": 2, "sales_marketing": 1}


# Función para calcular el coste total para contratar a los empleados
def calculate_total_cost(num_employees):
    engineers = (num_employees * ratio["engineers"]) // sum(ratio.values())
    journalists = (num_employees * ratio["journalists"]) // sum(ratio.values())
    sales_marketing = (num_employees * ratio["sales_marketing"]) // sum(ratio.values())

    # Calculate total salaries
    total_salaries = (
        engineers * salaries["full_stack_developer"]
        + engineers * salaries["ai_researcher"]
        + engineers * salaries["cloud_developer"]
        + journalists * salaries["journalist"]
        + sales_marketing * salaries["marketing_sales"]
    )

    total_social_security = total_salaries * social_security_rate
    total_cost = total_salaries + total_social_security

    return total_salaries, total_social_security, total_cost


growth_simulation = []
num_employees_list = range(
    2, 30
)  # Arrancamos con 2 desarrolladores, y pasamos hasta la etapa de tamaño PYME - 30

for num_employees in num_employees_list:
    total_salaries, total_social_security, total_cost = calculate_total_cost(
        num_employees
    )
    growth_simulation.append(
        {
            "num_employees": num_employees,
            "total_salaries": total_salaries,
            "total_social_security": total_social_security,
            "total_cost": total_cost,
        }
    )

# Convert to DataFrame
df = pd.DataFrame(growth_simulation)
df.head()

# Define the max number of hires per year
max_hires_per_year = 6

# Initialize lists to store the data for the graph
years = []
engineer_costs = []
journalist_costs = []
marketing_costs = []
social_security_costs = []

# Initialize lists to store the number of employees for the annotations
engineer_numbers = []
journalist_numbers = []
marketing_numbers = []


# Function to calculate individual department costs
def calculate_department_costs(num_engineers, num_journalists, num_sales_marketing):
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

    return (
        engineer_cost,
        journalist_cost,
        marketing_cost,
        social_security_cost,
        total_cost,
    )


# Simulate the hiring process over the years
num_employees = 2
year = 1

while num_employees <= 70:
    years.append(year)

    # Calculate the number of employees in each department based on the ratio
    num_engineers = (num_employees * ratio["engineers"]) // sum(ratio.values())
    num_journalists = (num_employees * ratio["journalists"]) // sum(ratio.values())
    num_sales_marketing = (num_employees * ratio["sales_marketing"]) // sum(
        ratio.values()
    )

    engineer_cost, journalist_cost, marketing_cost, social_security_cost, total_cost = (
        calculate_department_costs(num_engineers, num_journalists, num_sales_marketing)
    )

    engineer_costs.append(engineer_cost)
    journalist_costs.append(journalist_cost)
    marketing_costs.append(marketing_cost)
    social_security_costs.append(social_security_cost)

    # Store the number of employees for the annotations
    engineer_numbers.append(num_engineers)
    journalist_numbers.append(num_journalists)
    marketing_numbers.append(num_sales_marketing)

    # Increment the number of employees and year
    num_employees += max_hires_per_year
    year += 1

# Create traces for each department
fig = go.Figure()

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
            for i, j, k in zip(engineer_costs, journalist_costs, marketing_costs)
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

# Update layout for better readability
fig.update_layout(
    barmode="stack",
    title="Cost Progression for Team Growth",
    xaxis_title="Year",
    yaxis_title="Cost (€)",
    legend_title="Department",
    template="plotly_white",
)

fig.show()
