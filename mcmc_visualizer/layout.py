"""Layout components for the MCMC Visualizer dashboard."""

import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table

from .frequency import ITU_BAND_OPTIONS
from .data import get_allocations, get_unique_services
from .spectrum import SPECTRUM_VIEWPORT_HEIGHT_PX

BRAND_PURPLE = "#5B3B6B"
SECTION_BORDER = "#d7cfdf"
SECTION_SHADOW = "0 4px 14px rgba(62, 39, 78, 0.08)"
SECTION_RADIUS = "16px"
SECTION_PADDING = "14px 16px"

ALLOCATION_SECTION_STYLE = {
    "backgroundColor": "white",
    "border": f"1px solid {SECTION_BORDER}",
    "borderRadius": SECTION_RADIUS,
    "overflow": "hidden",
    "boxShadow": SECTION_SHADOW,
}

ALLOCATION_SECTION_HEADER_STYLE = {
    "backgroundColor": BRAND_PURPLE,
    "color": "white",
    "fontWeight": "700",
    "fontSize": "1.15rem",
    "lineHeight": "1.2",
    "padding": "12px 16px",
    "margin": 0,
}

ALLOCATION_SECTION_BODY_STYLE = {
    "backgroundColor": "white",
    "padding": SECTION_PADDING,
}

ALLOCATION_SIDEBAR_STYLE = {
    "height": "100%",
    "display": "flex",
    "flexDirection": "column",
    "gap": "16px",
}

ALLOCATION_CONTENT_COLUMN_STYLE = {
    "display": "flex",
    "flexDirection": "column",
    "gap": "16px",
}

ALLOCATION_SEGMENTED_GROUP_STYLE = {
    "width": "100%",
    "display": "flex",
    "gap": "0",
}

ALLOCATION_BANDS_SCROLL_STYLE = {
    "maxHeight": "320px",
    "overflowY": "auto",
    "paddingRight": "4px",
}

SPECTRUM_SERVICE_SCROLL_STYLE = {
    "maxHeight": "500px",
    "overflowY": "auto",
    "paddingRight": "4px",
}

ALLOCATION_TABLE_SECTION_BODY_STYLE = {
    **ALLOCATION_SECTION_BODY_STYLE,
    "padding": "12px 16px 16px 16px",
}

SPECTRUM_PANEL_BODY_STYLE = {
    **ALLOCATION_SECTION_BODY_STYLE,
    "padding": "12px 16px 16px 16px",
}


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


def create_allocation_section(title: str, content, body_style: dict | None = None):
    """Create a shared framed section for the Allocation tab."""
    merged_body_style = dict(ALLOCATION_SECTION_BODY_STYLE)
    if body_style:
        merged_body_style.update(body_style)

    return html.Div(
        [
            html.Div(title, style=ALLOCATION_SECTION_HEADER_STYLE),
            html.Div(content, style=merged_body_style),
        ],
        style=ALLOCATION_SECTION_STYLE,
    )


def create_allocation_sidebar():
    """Create the left sidebar for the Allocation tab."""
    allocations_df = get_allocations()
    services = get_unique_services(allocations_df)
    
    return html.Div(
        [
            create_allocation_section(
                "Allocation Name",
                dcc.Dropdown(
                    id="allocation-service-dropdown",
                    options=[{"label": s, "value": s} for s in services],
                    value=None,
                    multi=True,
                    placeholder="All",
                    clearable=True,
                ),
            ),
            create_allocation_section(
                "Primary or Secondary",
                dbc.ButtonGroup(
                    [
                        dbc.Button(
                            "Primary",
                            id="btn-primary",
                            color="primary",
                            outline=False,
                            active=True,
                            style={"width": "50%"},
                        ),
                        dbc.Button(
                            "Secondary",
                            id="btn-secondary",
                            color="secondary",
                            outline=False,
                            active=True,
                            style={"width": "50%"},
                        ),
                    ],
                    style=ALLOCATION_SEGMENTED_GROUP_STYLE,
                ),
            ),
            create_allocation_section(
                "Bands",
                dbc.Checklist(
                    id="band-checklist",
                    options=[{"label": b, "value": b} for b in ITU_BAND_OPTIONS[1:]],
                    value=[],
                    inline=False,
                ),
                body_style=ALLOCATION_BANDS_SCROLL_STYLE,
            ),
        ],
        style=ALLOCATION_SIDEBAR_STYLE,
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
            "backgroundColor": BRAND_PURPLE,
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
            "backgroundColor": BRAND_PURPLE,
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
            "backgroundColor": BRAND_PURPLE,
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
                        create_allocation_section(
                            "Allocations",
                            create_allocations_table(),
                            body_style=ALLOCATION_TABLE_SECTION_BODY_STYLE,
                        ),
                        create_allocation_section(
                            "Allocation Footnotes",
                            create_footnotes_table(),
                            body_style=ALLOCATION_TABLE_SECTION_BODY_STYLE,
                        ),
                        create_allocation_section(
                            "Applications which share the same Frequency Bands [Drill-through into Licences]",
                            create_applications_table(),
                            body_style=ALLOCATION_TABLE_SECTION_BODY_STYLE,
                        ),
                    ],
                    width=9,
                    style=ALLOCATION_CONTENT_COLUMN_STYLE,
                ),
            ],
            className="p-3",
        ),
    ])


def create_spectrum_sidebar():
    """Create the left sidebar for the Spectrum tab."""
    allocations_df = get_allocations()
    services = get_unique_services(allocations_df)
    
    return html.Div(
        [
            create_allocation_section(
                "Primary or Secondary",
                dbc.ButtonGroup(
                    [
                        dbc.Button(
                            "Primary",
                            id="spectrum-btn-primary",
                            color="primary",
                            outline=False,
                            active=True,
                            style={"width": "50%"},
                        ),
                        dbc.Button(
                            "Secondary",
                            id="spectrum-btn-secondary",
                            color="secondary",
                            outline=False,
                            active=True,
                            style={"width": "50%"},
                        ),
                    ],
                    style=ALLOCATION_SEGMENTED_GROUP_STYLE,
                ),
            ),
            create_allocation_section(
                "Allocation Name",
                dbc.Checklist(
                    id="spectrum-service-checklist",
                    options=[{"label": s, "value": s} for s in services],
                    value=services,  # All selected by default
                    inline=False,
                ),
                body_style=SPECTRUM_SERVICE_SCROLL_STYLE,
            ),
        ],
        style=ALLOCATION_SIDEBAR_STYLE,
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
                create_allocation_section(
                    "Spectrum",
                    html.Div(
                        dcc.Graph(
                            id="spectrum-chart",
                            responsive=False,
                            config={
                                "displayModeBar": False,
                                "scrollZoom": False,
                                "staticPlot": False,
                            },
                        ),
                        style={
                            "height": f"{SPECTRUM_VIEWPORT_HEIGHT_PX}px",
                            "overflowY": "scroll",
                            "overflowX": "hidden",
                        },
                    ),
                    body_style=SPECTRUM_PANEL_BODY_STYLE,
                ),
                width=7,
            ),
            dbc.Col(
                create_allocation_section(
                    "Legend",
                    html.Div(
                        id="spectrum-legend",
                        style={
                            "height": f"{SPECTRUM_VIEWPORT_HEIGHT_PX}px",
                            "overflowY": "auto",
                        },
                    ),
                    body_style=SPECTRUM_PANEL_BODY_STYLE,
                ),
                width=3,
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
