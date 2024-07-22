import dash
import dash_bootstrap_components as dbc

from layouts.main_layout import create_layout
from callbacks import register_callbacks

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Create the app layout
app.layout = create_layout()

# Register callbacks
register_callbacks(app)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)