import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px

# Initialize the Dash app with exception suppression
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Layout
app.layout = html.Div(
    style={'backgroundColor': '#007bff', 'height': '100vh', 'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'},
    children=[
        html.Div(
            style={'backgroundColor': 'white', 'width': '90%', 'height': '90%', 'display': 'flex'},
            children=[
                dbc.Tabs(
                    [
                        dbc.Tab(label="General", tab_id="general"),
                        dbc.Tab(label="Ad Revenue", tab_id="ad_revenue"),
                        dbc.Tab(label="Subscription Revenue", tab_id="subscription_revenue"),
                    ],
                    id="tabs",
                    active_tab="general",
                    style={'width': '20%', 'padding': '10px'}
                ),
                html.Div(id='parameters-content', style={'width': '20%', 'padding': '10px'}),
                html.Div(id='graph-content', style={'width': '60%', 'padding': '10px'}),
            ]
        )
    ]
)

# Callback to render the appropriate parameter inputs based on the selected tab
@app.callback(
    Output('parameters-content', 'children'),
    [Input('tabs', 'active_tab')]
)
def render_content(tab):
    if tab == 'general':
        return general_layout()
    elif tab == 'ad_revenue':
        return ad_revenue_layout()
    elif tab == 'subscription_revenue':
        return subscription_revenue_layout()
    return html.Div("Please select a tab")

def general_layout():
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Label("Year 1 User Base"),
                dbc.Input(id='year1_user_base', type='number', value=1000),
            ]),
            dbc.Col([
                dbc.Label("Year 2 User Base"),
                dbc.Input(id='year2_user_base', type='number', value=1200),
            ]),
            dbc.Col([
                dbc.Label("Year 3 User Base"),
                dbc.Input(id='year3_user_base', type='number', value=1400),
            ]),
            dbc.Col([
                dbc.Label("Year 4 User Base"),
                dbc.Input(id='year4_user_base', type='number', value=1600),
            ]),
            dbc.Col([
                dbc.Label("Year 5 User Base"),
                dbc.Input(id='year5_user_base', type='number', value=1800),
            ]),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Label("Percentage User Growth"),
                dbc.Input(id='percentage_user_growth', type='number', value=10),
            ]),
        ]),
    ])

def ad_revenue_layout():
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Label("CTR (Click-Through Rate)"),
                dbc.Input(id='ctr', type='number', value=2.0),
            ]),
            dbc.Col([
                dbc.Label("CPM (Cost Per Mille)"),
                dbc.Input(id='cpm', type='number', value=5.0),
            ]),
            dbc.Col([
                dbc.Label("CPC (Cost Per Click)"),
                dbc.Input(id='cpc', type='number', value=0.10),
            ]),
            dbc.Col([
                dbc.Label("Average ARPU (Average Revenue Per User)"),
                dbc.Input(id='arpu', type='number', value=1.0),
            ]),
        ]),
    ])

def subscription_revenue_layout():
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Label("Basic Users (%)"),
                dbc.Input(id='basic_users', type='number', value=70),
            ]),
            dbc.Col([
                dbc.Label("Curious Users (%)"),
                dbc.Input(id='curious_users', type='number', value=20),
            ]),
            dbc.Col([
                dbc.Label("Oracle Users (%)"),
                dbc.Input(id='oracle_users', type='number', value=10),
            ]),
        ]),
    ])

# Callback to update the graph based on input changes
@app.callback(
    Output('graph-content', 'children'),
    [
        Input('year1_user_base', 'value'),
        Input('year2_user_base', 'value'),
        Input('year3_user_base', 'value'),
        Input('year4_user_base', 'value'),
        Input('year5_user_base', 'value'),
        Input('percentage_user_growth', 'value'),
        Input('ctr', 'value'),
        Input('cpm', 'value'),
        Input('cpc', 'value'),
        Input('arpu', 'value'),
        Input('basic_users', 'value'),
        Input('curious_users', 'value'),
        Input('oracle_users', 'value')
    ]
)
def update_graph(year1, year2, year3, year4, year5, growth, ctr, cpm, cpc, arpu, basic, curious, oracle):
    ctx = dash.callback_context
    if not ctx.triggered:
        return html.Div("Please select a tab and enter parameters.")

    # User Base Growth Calculation
    user_base = [year1, year2, year3, year4, year5]

    # Ad Revenue Calculation
    ad_revenue = []
    for users in user_base:
        clicks = users * (ctr / 100)
        revenue = (clicks * cpc) + (users * (cpm / 1000) * arpu)
        ad_revenue.append(revenue)

    # Subscription Revenue Calculation
    subscription_revenue = []
    subscription_prices = {'basic': 0, 'curious': 4.99, 'oracle': 14.99}
    for users in user_base:
        basic_revenue = users * (basic / 100) * subscription_prices['basic']
        curious_revenue = users * (curious / 100) * subscription_prices['curious']
        oracle_revenue = users * (oracle / 100) * subscription_prices['oracle']
        total_subscription_revenue = basic_revenue + curious_revenue + oracle_revenue
        subscription_revenue.append(total_subscription_revenue)

    # Total Revenue
    total_revenue = [ad + sub for ad, sub in zip(ad_revenue, subscription_revenue)]

    # DataFrame for plotting
    data = {
        'Year': ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5'],
        'Ad Revenue': ad_revenue,
        'Subscription Revenue': subscription_revenue,
        'Total Revenue': total_revenue
    }

    df = pd.DataFrame(data)

    # Plotly Graph
    fig = px.bar(df, x='Year', y=['Ad Revenue', 'Subscription Revenue'], title='Year-over-Year Revenue')

    return dcc.Graph(figure=fig)

# Running the app
if __name__ == '__main__':
    app.run_server(debug=True)
