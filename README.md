# MCMC Frequency Allocation Visualizer

Interactive Dash dashboard for visualizing radio frequency allocations, services, and spectrum applications.

## Features

- **Allocation Tab**: Browse frequency allocations with filtering by service, status (primary/secondary), and frequency bands. Select a row to see associated footnotes and overlapping applications.
- **Spectrum Tab**: Visual stacked bar chart of frequency allocations by band. Click a segment to filter the Allocations table.
- **Global Frequency Filter**: Filter both tabs by ITU band (VLF, LF, MF, etc.) or specify custom frequency ranges.

## Installation

```bash
# Install dependencies using uv
uv sync

# Or using pip
pip install -e .
```

## Running the Dashboard

```bash
# Run the Dash app
python app.py

# Or use uv
uv run app.py
```

Then open your browser to http://localhost:8050

## Data Sources

The dashboard loads data from the `files/` directory:

- `footnotes_by_service.json` - Frequency allocations with band ranges, services, and footnote references
- `footnote.json` - Footnote text details by allocation ID  
- `spectrum.json` - Spectrum applications with frequency bands and conditions

## Data Access

If you need the data for this visualizer, contact Shai.

## Project Structure

```
.
├── app.py                    # Dash app entry point
├── mcmc_visualizer/
│   ├── __init__.py
│   ├── callbacks.py          # Dash callbacks for interactivity
│   ├── data.py               # Data loading and normalization
│   ├── frequency.py          # Frequency parsing and ITU band utilities
│   └── layout.py             # Dashboard layout components
├── files/                    # Data files
├── docs/                     # UI mockup images
└── pyproject.toml
```
