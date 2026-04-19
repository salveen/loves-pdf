"""Layout definition for the Priva PDF application."""

from dash import dcc, html
import dash_bootstrap_components as dbc


def create_layout() -> html.Div:
    """Create the main application layout."""
    return html.Div([
        html.Div([
            # Header
            html.Div([
                html.H1("Priva PDF"),
                html.P("Private, local PDF tools — your files never leave your machine"),
            ], className="main-header"),
            
            # Tabs
            dbc.Tabs([
                dbc.Tab(label="Merge PDFs", tab_id="tab-merge"),
                dbc.Tab(label="Split PDF", tab_id="tab-split"),
                dbc.Tab(label="Compress PDF", tab_id="tab-compress"),
            ], id="tabs", active_tab="tab-merge"),
            
            # Tab content
            html.Div(id="tab-content"),
            
            # Footer
            html.Div([
                html.Div("🔒 100% Private — All processing happens locally", className="privacy-badge"),
                html.P("Your files never leave your machine", style={"marginTop": "1rem", "fontSize": "0.8rem"}),
            ], className="footer"),
            
        ], className="main-container"),
        
        # Storage for file data
        dcc.Store(id="merge-files-store", data=[]),
        dcc.Store(id="compress-file-store", data=None),
        dcc.Store(id="split-file-store", data=None),
    ], style={"minHeight": "100vh"})
