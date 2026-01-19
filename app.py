"""Main Dash application entry point."""

import dash
import dash_bootstrap_components as dbc

from mcmc_visualizer.layout import create_layout
from mcmc_visualizer.callbacks import register_callbacks
from mcmc_visualizer.data import reload_all_data

# Initialize Dash app with Bootstrap theme
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

# Set the app title
app.title = "MCMC Frequency Allocation Dashboard"

# Load data on startup
reload_all_data()

# Set the layout
app.layout = create_layout()

# Register all callbacks
register_callbacks(app)

# Expose the Flask server for deployment
server = app.server

if __name__ == "__main__":
    app.run(debug=True, port=8050)
