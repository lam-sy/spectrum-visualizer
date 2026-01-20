"""Layout components for the MCMC Visualizer dashboard."""

import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table

from .frequency import ITU_BAND_OPTIONS
from .data import get_allocations, get_unique_services

# Color palette for services (matches the mockup)
SERVICE_COLORS = {
    "Aeronautical Mobile": "#8B4B7C",
    "Aeronautical Mobile (OR)": "#A05B8C",
    "Aeronautical Mobile (R)": "#C46B9C",
    "Aeronautical Mobile-Satellite (R)": "#4BA3A3",
    "Aeronautical Radionavigation": "#5B3B6B",
    "Amateur": "#C4A000",
    "Amateur-Satellite": "#D4B010",
    "Broadcasting": "#D4497A",
    "Broadcasting-Satellite": "#9B2D5B",
    "Earth Exploration-Satellite": "#6BA35B",
    "Earth Exploration-Satellite (active)": "#5B934B",
    "Earth Exploration-Satellite (passive)": "#8BC37B",
    "Fixed": "#D46B8B",
    "Fixed-Satellite": "#F4A3B3",
    "Inter-Satellite": "#3B7B8B",
    "Land Mobile": "#E4A040",
    "Maritime Mobile": "#3B8BBB",
    "Maritime Mobile-Satellite": "#2B6B9B",
    "Maritime Radionavigation": "#4B5B7B",
    "Meteorological Aids": "#6B4B6B",
    "Meteorological-Satellite": "#8B5B8B",
    "Mobile": "#D4D060",
    "Mobile (distress and calling)": "#E4E080",
    "Mobile except aeronautical mobile": "#C4C050",
    "Mobile except aeronautical mobile (R)": "#B4B040",
    "Mobile-Satellite": "#7BB0C0",
    "Not Allocated": "#808080",
    "(Not allocated)": "#808080",
    "Radio Astronomy": "#5B5BA0",
    "Radiodetermination-Satellite": "#9B4B6B",
    "Radiolocation": "#7B6B9B",
    "Radiolocation-Satellite": "#8B7BAB",
    "Radionavigation": "#6B5B8B",
    "Radionavigation-Satellite": "#7B6B9B",
    "Space Operation": "#4B8B6B",
    "Space Research": "#3B7B5B",
    "Standard Frequency and Time Signal": "#AB8B3B",
    "STANDARD FREQUENCY AND TIME SIGNAL": "#AB8B3B",
}

# Default color for unknown services
DEFAULT_COLOR = "#888888"


def get_service_color(service: str) -> str:
    """Get color for a service, using default if not found."""
    # Check exact match first
    if service in SERVICE_COLORS:
        return SERVICE_COLORS[service]
    
    # Check case-insensitive match
    service_lower = service.lower()
    for key, color in SERVICE_COLORS.items():
        if key.lower() == service_lower:
            return color
    
    # Check partial match
    for key, color in SERVICE_COLORS.items():
        if key.lower() in service_lower or service_lower in key.lower():
            return color
    
    return DEFAULT_COLOR


def create_frequency_filter_row():
    """Create the top frequency filter row per filter_example.png."""
    return dbc.Row(
        [
            dbc.Col(
                [
                    html.Label("Choose a predefined range", className="me-2"),
                    dcc.Dropdown(
                        id="itu-band-dropdown",
                        options=[{"label": b, "value": b} for b in ITU_BAND_OPTIONS],
                        value="All",
                        clearable=False,
                        style={"minWidth": "200px"},
                    ),
                ],
                width="auto",
                className="d-flex align-items-center",
            ),
            dbc.Col(
                html.Label("or specific frequencies", className="mx-3"),
                width="auto",
                className="d-flex align-items-center",
            ),
            dbc.Col(
                [
                    dbc.Input(
                        id="freq-from-input",
                        type="number",
                        placeholder="",
                        style={"width": "100px"},
                    ),
                ],
                width="auto",
            ),
            dbc.Col(
                dcc.Dropdown(
                    id="freq-from-unit",
                    options=[
                        {"label": "Hz", "value": "Hz"},
                        {"label": "kHz", "value": "kHz"},
                        {"label": "MHz", "value": "MHz"},
                        {"label": "GHz", "value": "GHz"},
                        {"label": "THz", "value": "THz"},
                    ],
                    value="MHz",
                    clearable=False,
                    style={"width": "80px"},
                ),
                width="auto",
            ),
            dbc.Col(
                html.Label("to", className="mx-2"),
                width="auto",
                className="d-flex align-items-center",
            ),
            dbc.Col(
                [
                    dbc.Input(
                        id="freq-to-input",
                        type="number",
                        placeholder="",
                        style={"width": "100px"},
                    ),
                ],
                width="auto",
            ),
            dbc.Col(
                dcc.Dropdown(
                    id="freq-to-unit",
                    options=[
                        {"label": "Hz", "value": "Hz"},
                        {"label": "kHz", "value": "kHz"},
                        {"label": "MHz", "value": "MHz"},
                        {"label": "GHz", "value": "GHz"},
                        {"label": "THz", "value": "THz"},
                    ],
                    value="MHz",
                    clearable=False,
                    style={"width": "80px"},
                ),
                width="auto",
            ),
        ],
        className="mb-3 p-3 bg-light align-items-center",
    )


def create_allocation_sidebar():
    """Create the left sidebar for the Allocation tab."""
    allocations_df = get_allocations()
    services = get_unique_services(allocations_df)
    
    return dbc.Card(
        [
            dbc.CardHeader("Allocation Name"),
            dbc.CardBody(
                [
                    dcc.Dropdown(
                        id="allocation-service-dropdown",
                        options=[{"label": s, "value": s} for s in services],
                        value=None,
                        multi=True,
                        placeholder="All",
                    ),
                ]
            ),
            dbc.CardHeader("Primary or Secondary", className="mt-2"),
            dbc.CardBody(
                dbc.ButtonGroup(
                    [
                        dbc.Button(
                            "Primary",
                            id="btn-primary",
                            color="primary",
                            outline=False,
                            active=True,
                            className="me-1",
                        ),
                        dbc.Button(
                            "Secondary",
                            id="btn-secondary",
                            color="secondary",
                            outline=False,
                            active=True,
                        ),
                    ],
                    className="w-100",
                ),
            ),
            dbc.CardHeader("Bands", className="mt-2"),
            dbc.CardBody(
                dbc.Checklist(
                    id="band-checklist",
                    options=[{"label": b, "value": b} for b in ITU_BAND_OPTIONS[1:]],  # Skip "All"
                    value=[],  # All selected by default (empty = all)
                    inline=False,
                ),
                style={"maxHeight": "300px", "overflowY": "auto"},
            ),
        ],
        style={"height": "100%"},
    )


def create_allocations_table():
    """Create the Allocations DataTable."""
    return dash_table.DataTable(
        id="allocations-table",
        columns=[
            {"name": "Allocation Frequency", "id": "band_label"},
            {"name": "Allocation Name", "id": "service"},
            {"name": "Primary or Secondary Service", "id": "status"},
            {"name": "Footnote Numbers", "id": "footnotes_display"},
        ],
        data=[],
        page_action="none",
        style_table={"height": "400px", "overflowY": "auto"},
        style_header={
            "backgroundColor": "#5B3B6B",
            "color": "white",
            "fontWeight": "bold",
            "position": "sticky",
            "top": 0,
            "zIndex": 1,
        },
        style_cell={
            "textAlign": "left",
            "padding": "8px",
            "fontSize": "14px",
            "minWidth": "100px",
        },
        style_data_conditional=[
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "#f8f9fa",
            },
        ],
        sort_action="native",
        filter_action="native",
    )


def create_footnotes_table():
    """Create the Allocation Footnotes DataTable."""
    return dash_table.DataTable(
        id="footnotes-table",
        columns=[
            {"name": "Footnote Number", "id": "footnote_number"},
            {"name": "Footnote Text", "id": "footnote_text"},
        ],
        data=[],
        page_action="none",
        style_table={"height": "250px", "overflowY": "auto"},
        style_header={
            "backgroundColor": "#5B3B6B",
            "color": "white",
            "fontWeight": "bold",
            "position": "sticky",
            "top": 0,
            "zIndex": 1,
        },
        style_cell={
            "textAlign": "left",
            "padding": "8px",
            "fontSize": "14px",
            "whiteSpace": "normal",
            "height": "auto",
        },
        style_data_conditional=[
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "#f8f9fa",
            },
        ],
        sort_action="native",
        filter_action="native",
    )


def create_applications_table():
    """Create the Applications overlap DataTable."""
    return dash_table.DataTable(
        id="applications-table",
        columns=[
            {"name": "Application Frequency", "id": "frequency_bands"},
            {"name": "Application Name", "id": "applications"},
            {"name": "Application Method", "id": "max_power"},
            {"name": "Availability", "id": "remarks"},
        ],
        data=[],
        page_size=5,
        style_table={"overflowX": "auto"},
        style_header={
            "backgroundColor": "#5B3B6B",
            "color": "white",
            "fontWeight": "bold",
        },
        style_cell={
            "textAlign": "left",
            "padding": "8px",
            "fontSize": "14px",
            "whiteSpace": "normal",
            "height": "auto",
        },
        style_data_conditional=[
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "#f8f9fa",
            },
        ],
    )


def create_allocation_tab():
    """Create the Allocation tab content."""
    return html.Div([
        # Store for the currently selected allocation row index
        dcc.Store(id="allocations-selected-row", data=None),
        dbc.Row(
            [
                dbc.Col(
                    create_allocation_sidebar(),
                    width=3,
                    className="pe-3",
                ),
                dbc.Col(
                    [
                        html.H5("Allocations", className="mb-3"),
                        create_allocations_table(),
                        html.H5("Allocation Footnotes", className="mt-4 mb-3"),
                        create_footnotes_table(),
                        html.H5(
                            "Applications which share the same Frequency Bands [Drill-through into Licences]",
                            className="mt-4 mb-3",
                        ),
                        create_applications_table(),
                    ],
                    width=9,
                ),
            ],
            className="p-3",
        ),
    ])


def create_spectrum_sidebar():
    """Create the left sidebar for the Spectrum tab."""
    allocations_df = get_allocations()
    services = get_unique_services(allocations_df)
    
    return dbc.Card(
        [
            dbc.CardHeader("Primary or Secondary"),
            dbc.CardBody(
                dbc.ButtonGroup(
                    [
                        dbc.Button(
                            "Primary",
                            id="spectrum-btn-primary",
                            color="primary",
                            outline=False,
                            active=True,
                            className="me-1",
                        ),
                        dbc.Button(
                            "Secondary",
                            id="spectrum-btn-secondary",
                            color="secondary",
                            outline=False,
                            active=True,
                        ),
                    ],
                    className="w-100",
                ),
            ),
            dbc.CardHeader("Allocation Name", className="mt-2"),
            dbc.CardBody(
                dbc.Checklist(
                    id="spectrum-service-checklist",
                    options=[{"label": s, "value": s} for s in services],
                    value=services,  # All selected by default
                    inline=False,
                ),
                style={"maxHeight": "500px", "overflowY": "auto"},
            ),
        ],
        style={"height": "100%"},
    )


def create_spectrum_tab():
    """Create the Spectrum tab content."""
    return dbc.Row(
        [
            dbc.Col(
                create_spectrum_sidebar(),
                width=2,
                className="pe-3",
            ),
            dbc.Col(
                html.Div(
                    dcc.Graph(
                        id="spectrum-chart",
                        config={
                            "displayModeBar": False,
                            "scrollZoom": False,
                            "staticPlot": False,
                        },
                    ),
                    style={"height": "75vh", "overflowY": "scroll", "overflowX": "hidden"},
                ),
                width=7,
            ),
            dbc.Col(
                html.Div(id="spectrum-legend"),
                width=3,
                style={"height": "75vh", "overflowY": "auto"},
            ),
        ],
        className="p-3",
    )


def create_layout():
    """Create the main dashboard layout."""
    return dbc.Container(
        [
            # Store for selected spectrum band/service (for cross-tab linking)
            dcc.Store(id="spectrum-selection-store"),
            
            # Header
            html.H2("Frequency Allocation Dashboard", className="my-3"),
            
            # Top frequency filter row
            create_frequency_filter_row(),
            
            # Tabs
            dbc.Tabs(
                [
                    dbc.Tab(
                        create_allocation_tab(),
                        label="Allocation",
                        tab_id="tab-allocation",
                    ),
                    dbc.Tab(
                        create_spectrum_tab(),
                        label="Spectrum",
                        tab_id="tab-spectrum",
                    ),
                ],
                id="main-tabs",
                active_tab="tab-allocation",
                className="mb-3",
            ),
        ],
        fluid=True,
    )
