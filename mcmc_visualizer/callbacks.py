"""Dash callbacks for interactivity and data filtering."""

from dash import Input, Output, State, callback, no_update, html
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from .data import (
    get_allocations,
    get_footnotes,
    get_applications,
    get_footnotes_for_ids,
    get_overlapping_applications,
    get_unique_services,
)
from .frequency import (
    value_with_unit_to_hz,
    ITU_BANDS,
    ranges_overlap,
    format_frequency,
)
from .layout import get_service_color


def filter_allocations_by_frequency(
    df: pd.DataFrame,
    itu_band: str,
    freq_from: float | None,
    freq_from_unit: str,
    freq_to: float | None,
    freq_to_unit: str,
) -> pd.DataFrame:
    """Apply frequency filtering to allocations DataFrame."""
    if df.empty:
        return df
    
    # Determine filter range
    filter_start_hz = None
    filter_end_hz = None
    
    # Custom range takes precedence
    if freq_from is not None and freq_to is not None:
        filter_start_hz = value_with_unit_to_hz(freq_from, freq_from_unit)
        filter_end_hz = value_with_unit_to_hz(freq_to, freq_to_unit)
    elif itu_band and itu_band != "All" and itu_band in ITU_BANDS:
        filter_start_hz, filter_end_hz = ITU_BANDS[itu_band]
    
    # Apply filter if we have a range
    if filter_start_hz is not None and filter_end_hz is not None:
        mask = df.apply(
            lambda row: ranges_overlap(
                filter_start_hz, filter_end_hz,
                row["band_start_hz"], row["band_end_hz"]
            ),
            axis=1
        )
        return pd.DataFrame(df[mask])
    
    return df


def filter_allocations_by_service(
    df: pd.DataFrame,
    selected_services: list | None,
) -> pd.DataFrame:
    """Filter allocations by selected services."""
    if df.empty:
        return df
    
    if selected_services:
        return pd.DataFrame(df[df["service"].isin(selected_services)])
    
    return df


def filter_allocations_by_status(
    df: pd.DataFrame,
    show_primary: bool,
    show_secondary: bool,
) -> pd.DataFrame:
    """Filter allocations by primary/secondary status."""
    if df.empty:
        return df
    
    if show_primary and show_secondary:
        return df
    elif show_primary:
        return pd.DataFrame(df[df["status"] == "primary"])
    elif show_secondary:
        return pd.DataFrame(df[df["status"] == "secondary"])
    else:
        return pd.DataFrame(columns=df.columns)


def register_callbacks(app):
    """Register all Dash callbacks."""
    
    # Primary/Secondary button toggle for Allocation tab
    @callback(
        [Output("btn-primary", "active"), Output("btn-secondary", "active")],
        [Input("btn-primary", "n_clicks"), Input("btn-secondary", "n_clicks")],
        [State("btn-primary", "active"), State("btn-secondary", "active")],
        prevent_initial_call=True,
    )
    def toggle_allocation_status_buttons(n_primary, n_secondary, primary_active, secondary_active):
        from dash import ctx
        
        if ctx.triggered_id == "btn-primary":
            return not primary_active, secondary_active
        elif ctx.triggered_id == "btn-secondary":
            return primary_active, not secondary_active
        return primary_active, secondary_active

    @callback(
        [Output("btn-primary", "style"), Output("btn-secondary", "style")],
        [Input("btn-primary", "active"), Input("btn-secondary", "active")],
    )
    def update_allocation_button_styles(primary_active, secondary_active):
        active_style = {"backgroundColor": "#0d6efd", "borderColor": "#0d6efd", "color": "white"}
        inactive_style = {"backgroundColor": "#6c757d", "borderColor": "#6c757d", "color": "white"}
        return active_style if primary_active else inactive_style, active_style if secondary_active else inactive_style
    
    # Primary/Secondary button toggle for Spectrum tab
    @callback(
        [Output("spectrum-btn-primary", "active"), Output("spectrum-btn-secondary", "active")],
        [Input("spectrum-btn-primary", "n_clicks"), Input("spectrum-btn-secondary", "n_clicks")],
        [State("spectrum-btn-primary", "active"), State("spectrum-btn-secondary", "active")],
        prevent_initial_call=True,
    )
    def toggle_spectrum_status_buttons(n_primary, n_secondary, primary_active, secondary_active):
        from dash import ctx
        
        if ctx.triggered_id == "spectrum-btn-primary":
            return not primary_active, secondary_active
        elif ctx.triggered_id == "spectrum-btn-secondary":
            return primary_active, not secondary_active
        return primary_active, secondary_active

    @callback(
        [Output("spectrum-btn-primary", "style"), Output("spectrum-btn-secondary", "style")],
        [Input("spectrum-btn-primary", "active"), Input("spectrum-btn-secondary", "active")],
    )
    def update_spectrum_button_styles(primary_active, secondary_active):
        active_style = {"backgroundColor": "#0d6efd", "borderColor": "#0d6efd", "color": "white"}
        inactive_style = {"backgroundColor": "#6c757d", "borderColor": "#6c757d", "color": "white"}
        return active_style if primary_active else inactive_style, active_style if secondary_active else inactive_style
    
    # Toggle row selection using a store (click same row again to deselect)
    @callback(
        Output("allocations-selected-row", "data"),
        [Input("allocations-table", "active_cell")],
        [State("allocations-selected-row", "data")],
        prevent_initial_call=True,
    )
    def toggle_row_selection(active_cell, current_selected):
        if not active_cell:
            return current_selected
        
        clicked_row = active_cell.get("row")
        if clicked_row is None:
            return current_selected
        
        # If clicking the same row that's already selected, deselect it
        if current_selected is not None and clicked_row == current_selected:
            return None
        
        # Otherwise select the clicked row
        return clicked_row
    
    # Main callback: Update allocations table based on all filters
    @callback(
        Output("allocations-table", "data"),
        [
            Input("itu-band-dropdown", "value"),
            Input("freq-from-input", "value"),
            Input("freq-from-unit", "value"),
            Input("freq-to-input", "value"),
            Input("freq-to-unit", "value"),
            Input("allocation-service-dropdown", "value"),
            Input("btn-primary", "active"),
            Input("btn-secondary", "active"),
            Input("band-checklist", "value"),
            Input("spectrum-selection-store", "data"),
        ],
    )
    def update_allocations_table(
        itu_band, freq_from, freq_from_unit, freq_to, freq_to_unit,
        selected_services, show_primary, show_secondary, band_checklist,
        spectrum_selection
    ):
        df = get_allocations()
        
        # Apply frequency filter
        df = filter_allocations_by_frequency(
            df, itu_band, freq_from, freq_from_unit, freq_to, freq_to_unit
        )
        
        # Apply service filter
        df = filter_allocations_by_service(df, selected_services)
        
        # Apply status filter
        df = filter_allocations_by_status(df, show_primary, show_secondary)
        
        # Apply ITU band checklist filter
        if band_checklist:
            df = pd.DataFrame(df[df["itu_band"].isin(band_checklist)])
        
        # If spectrum selection is active, further filter to that range+service
        if spectrum_selection:
            sel_start = spectrum_selection.get("band_start_hz")
            sel_end = spectrum_selection.get("band_end_hz")
            sel_service = spectrum_selection.get("service")
            
            if sel_start and sel_end:
                mask = df.apply(
                    lambda row: ranges_overlap(
                        sel_start, sel_end,
                        row["band_start_hz"], row["band_end_hz"]
                    ),
                    axis=1
                )
                df = pd.DataFrame(df[mask])
            
            if sel_service:
                df = pd.DataFrame(df[df["service"] == sel_service])
        
        # Prepare display data
        display_df = df.copy()
        display_df["footnotes_display"] = display_df["footnote_ids"].apply(
            lambda ids: ", ".join(ids) if ids else ""
        )
        # Store footnote_ids as JSON string since DataTable only accepts scalar values
        display_df["footnote_ids_json"] = display_df["footnote_ids"].apply(
            lambda ids: ",".join(ids) if ids else ""
        )
        
        return display_df[["band_label", "service", "status", "footnotes_display", "band_start_hz", "band_end_hz", "footnote_ids_json"]].to_dict("records")
    
    # Update footnotes table when allocation row is selected
    @callback(
        Output("footnotes-table", "data"),
        [Input("allocations-selected-row", "data"),
         Input("allocations-table", "data")],
    )
    def update_footnotes_table(selected_row, table_data):
        footnotes_dict = get_footnotes()
        
        # If a row is selected, show only its footnotes
        if selected_row is not None and table_data and selected_row < len(table_data):
            row = table_data[selected_row]
            # Parse footnote_ids from comma-separated string
            footnote_ids_str = row.get("footnote_ids_json", "")
            footnote_ids = [x.strip() for x in footnote_ids_str.split(",") if x.strip()]
            
            if footnote_ids:
                footnotes_df = get_footnotes_for_ids(footnote_ids, footnotes_dict)
                return footnotes_df.to_dict("records")
        
        # No selection - show all footnotes from current filtered allocations
        if table_data:
            all_footnote_ids = set()
            for row in table_data:
                footnote_ids_str = row.get("footnote_ids_json", "")
                ids = [x.strip() for x in footnote_ids_str.split(",") if x.strip()]
                all_footnote_ids.update(ids)
            
            if all_footnote_ids:
                footnotes_df = get_footnotes_for_ids(list(all_footnote_ids), footnotes_dict)
                return footnotes_df.to_dict("records")
        
        return []
    
    # Update applications table when allocation row is selected
    @callback(
        Output("applications-table", "data"),
        [Input("allocations-selected-row", "data")],
        [State("allocations-table", "data")],
    )
    def update_applications_table(selected_row, table_data):
        if not table_data or selected_row is None:
            return []
        
        if selected_row >= len(table_data):
            return []
        
        row = table_data[selected_row]
        band_start = row.get("band_start_hz", 0)
        band_end = row.get("band_end_hz", 0)
        
        if not band_start or not band_end:
            return []
        
        apps_df = get_applications()
        overlapping = get_overlapping_applications(band_start, band_end, apps_df)
        
        return overlapping[["frequency_bands", "applications", "max_power", "remarks"]].to_dict("records")
    
    # Update allocations table row highlight based on selected row
    @callback(
        Output("allocations-table", "style_data_conditional"),
        [Input("allocations-selected-row", "data")],
    )
    def update_allocations_row_highlight(selected_row):
        # Base styling: odd rows have a light background
        base_styles = [
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "#f8f9fa",
            },
        ]
        
        # If a row is selected, add highlight styling for that row
        if selected_row is not None:
            base_styles.append({
                "if": {"row_index": selected_row},
                "backgroundColor": "#d4e5f7",
                "border": "1px solid #5B3B6B",
            })
        
        return base_styles
    
    # Update spectrum chart
    @callback(
        Output("spectrum-chart", "figure"),
        [
            Input("itu-band-dropdown", "value"),
            Input("freq-from-input", "value"),
            Input("freq-from-unit", "value"),
            Input("freq-to-input", "value"),
            Input("freq-to-unit", "value"),
            Input("spectrum-btn-primary", "active"),
            Input("spectrum-btn-secondary", "active"),
            Input("spectrum-service-checklist", "value"),
        ],
    )
    def update_spectrum_chart(
        itu_band, freq_from, freq_from_unit, freq_to, freq_to_unit,
        show_primary, show_secondary, selected_services
    ):
        df = get_allocations()
        
        # Apply frequency filter
        df = filter_allocations_by_frequency(
            df, itu_band, freq_from, freq_from_unit, freq_to, freq_to_unit
        )
        
        # Apply service filter
        if selected_services:
            df = pd.DataFrame(df[df["service"].isin(selected_services)])
        
        # Apply status filter
        df = filter_allocations_by_status(df, show_primary, show_secondary)
        
        if df.empty:
            return go.Figure()
        
        # Group by unique frequency bands
        bands = df.groupby(["band_start_hz", "band_end_hz"]).agg({
            "service": list,
            "status": list,
            "band_label": "first",
        }).reset_index()
        
        # Sort by start frequency
        bands = bands.sort_values("band_start_hz").reset_index(drop=True)
        
        # Create figure
        fig = go.Figure()
        
        # Track which services we've already added to legend
        legend_shown = set()
        
        # Build stacked bar chart
        for _, row in bands.iterrows():
            services = row["service"]
            band_label = row["band_label"]
            band_start = row["band_start_hz"]
            band_end = row["band_end_hz"]
            
            # Calculate segment width for each service
            num_services = len(services)
            
            for service in services:
                color = get_service_color(service)
                
                # Only show in legend if we haven't seen this service yet
                show_in_legend = service not in legend_shown
                if show_in_legend:
                    legend_shown.add(service)
                
                # Add a bar segment for this service
                fig.add_trace(go.Bar(
                    y=[band_label],
                    x=[1 / num_services],  # Equal width for each service in the band
                    orientation="h",
                    marker_color=color,
                    name=service,
                    legendgroup=service,
                    showlegend=show_in_legend,
                    hovertemplate=f"<b>{service}</b><br>{band_label}<extra></extra>",
                    customdata=[[band_start, band_end, service]],
                ))
        
        # Update layout
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
            height=len(bands) * 30,
            plot_bgcolor="white",
            dragmode=False,
        )
        
        # Build legend data for custom legend component
        legend_items = []
        for service in sorted(legend_shown):
            legend_items.append({
                "service": service,
                "color": get_service_color(service),
            })
        
        return fig
    
    # Render custom legend
    @callback(
        Output("spectrum-legend", "children"),
        [Input("spectrum-chart", "figure")],
    )
    def render_spectrum_legend(figure):
        if not figure or "data" not in figure:
            return []
        
        # Extract unique services and colors from traces
        seen = {}
        for trace in figure.get("data", []):
            name = trace.get("name")
            color = trace.get("marker", {}).get("color")
            if name and color and name not in seen:
                seen[name] = color
        
        # Build legend items
        items = []
        for service, color in sorted(seen.items()):
            items.append(
                html.Div(
                    [
                        html.Span(
                            style={
                                "display": "inline-block",
                                "width": "16px",
                                "height": "16px",
                                "backgroundColor": color,
                                "marginRight": "8px",
                                "borderRadius": "2px",
                            }
                        ),
                        html.Span(service, style={"fontSize": "12px"}),
                    ],
                    style={"display": "flex", "alignItems": "center", "marginBottom": "6px"},
                )
            )
        
        return items
    
    # Handle spectrum chart click to update selection store
    @callback(
        Output("spectrum-selection-store", "data"),
        [Input("spectrum-chart", "clickData")],
        prevent_initial_call=True,
    )
    def handle_spectrum_click(click_data):
        if not click_data:
            return None
        
        point = click_data.get("points", [{}])[0]
        customdata = point.get("customdata", [])
        
        if len(customdata) >= 3:
            return {
                "band_start_hz": customdata[0],
                "band_end_hz": customdata[1],
                "service": customdata[2],
            }
        
        return None
    
    # Switch to Allocation tab when spectrum is clicked
    @callback(
        Output("main-tabs", "active_tab"),
        [Input("spectrum-selection-store", "data")],
        prevent_initial_call=True,
    )
    def switch_to_allocation_on_click(spectrum_selection):
        if spectrum_selection:
            return "tab-allocation"
        return no_update
