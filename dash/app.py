"""
Priva PDF - Private, local PDF tools.

Run with: python app.py
"""

from dash import Dash
import dash_bootstrap_components as dbc

from app.styles import get_index_string
from app.layout import create_layout

# Import callbacks to register them with the app
import app.callbacks  # noqa: F401

# Initialize Dash app
dash_app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True,
    title="Priva PDF",
)

# Apply custom styling
dash_app.index_string = get_index_string()

# Set layout
dash_app.layout = create_layout()

# Server for deployment (e.g., Gunicorn)
server = dash_app.server

if __name__ == "__main__":
    dash_app.run(debug=True, host="0.0.0.0", port=8050)
