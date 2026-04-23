"""Spectrum chart styling and figure construction."""

import pandas as pd
import plotly.graph_objects as go

# Scroll-based spectrum viewport tuning.
SPECTRUM_ROW_HEIGHT_PX = 42
SPECTRUM_VIEWPORT_HEIGHT_PX = 720

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
    if service in SERVICE_COLORS:
        return SERVICE_COLORS[service]

    service_lower = service.lower()
    for key, color in SERVICE_COLORS.items():
        if key.lower() == service_lower:
            return color

    for key, color in SERVICE_COLORS.items():
        if key.lower() in service_lower or service_lower in key.lower():
            return color

    return DEFAULT_COLOR


def build_spectrum_figure(df: pd.DataFrame) -> go.Figure:
    """Build the scroll-first spectrum figure from filtered allocations."""
    if df.empty:
        return go.Figure().update_layout(
            height=SPECTRUM_VIEWPORT_HEIGHT_PX,
            plot_bgcolor="white",
        )

    bands = df.groupby(["band_start_hz", "band_end_hz"]).agg({
        "service": list,
        "status": list,
        "band_label": "first",
    }).reset_index()
    bands = bands.sort_values("band_start_hz").reset_index(drop=True)

    fig = go.Figure()
    legend_shown = set()

    for _, row in bands.iterrows():
        services = row["service"]
        band_label = row["band_label"]
        band_start = row["band_start_hz"]
        band_end = row["band_end_hz"]
        num_services = len(services)

        for service in services:
            show_in_legend = service not in legend_shown
            if show_in_legend:
                legend_shown.add(service)

            fig.add_trace(go.Bar(
                y=[band_label],
                x=[1 / num_services],
                orientation="h",
                marker_color=get_service_color(service),
                name=service,
                legendgroup=service,
                showlegend=show_in_legend,
                hovertemplate=f"<b>{service}</b><br>{band_label}<extra></extra>",
                customdata=[[band_start, band_end, service]],
            ))

    fig.update_layout(
        barmode="stack",
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            fixedrange=True,
        ),
        yaxis=dict(
            title="",
            autorange="reversed",
            tickfont=dict(size=11),
            fixedrange=True,
        ),
        showlegend=False,
        margin=dict(l=160, r=10, t=10, b=10),
        height=len(bands) * SPECTRUM_ROW_HEIGHT_PX,
        plot_bgcolor="white",
        dragmode=False,
    )

    return fig
