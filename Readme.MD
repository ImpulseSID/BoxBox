# BoxBox - F1 Telemetry Analysis

**BoxBox** is a Python-based toolkit for analyzing and visualizing Formula 1 telemetry data. Built on top of [FastF1](https://github.com/theOehrly/Fast-F1) and [Plotly](https://plotly.com/python/), it generates interactive, high-resolution HTML charts to analyze driver performance, track dominance, and speed traces.

## Features

- **🏎️ Interactive Speed Traces:** Compare telemetry for every driver across an entire race.
- **🗺️ Track Dominance Maps:** Visualize exactly where one driver is faster than another in a race Qualifying.

- **⚡ Local Caching:** Optimized with FastF1 caching to minimize download times for repeat analyses.

## Project Structure

```text
BOXBOX/
├── cache/                 # FastF1 data cache (auto-generated)
├── dominance_maps/        # Output folder for Dominance Map HTMLs
├── speed_trace/           # Output folder for Speed Trace HTMLs
├── src/                   # Source code
│   ├── dominance_map.py   # Generates Track Dominance Maps
│   ├── speed_trace.py     # Generates Interactive Speed Traces
│   ├── get_data.py        # Helper for fetching raw data
│   └── export_data.py     # Helper for exporting CSVs
├── .venv/                 # Python Virtual Environment
└── README.md              # This file
```

## Installation

- Clone or Open the Project Ensure you are in the root directory BoxBox.
- Set up Virtual Environment

```
python -m venv .venv

For Windows:
.venv\Scripts\activate

For Mac/Linux:
source .venv/bin/activate
```

# Install Core Dependencies

```
pip install fastf1 pandas plotly matplotlib
```

# Usage

### Track Dominance Map

* This tool compares the top 2 fastest drivers in a Qualifying session and paints the track map based on who was faster in each 10m mini-sector.

### Interactive Speed Trace

* This tool creates a slider-controlled line chart to compare speed vs. distance for all drivers on any lap.

# Configuration

* Cache: The cache is stored in the /cache folder. If you encounter data corruption errors, simply delete this folder, and the scripts will re-download fresh data.

* Chunk Size: You can adjust the resolution of the dominance map by changing chunk_size = 10 in src/dominance_map.py.