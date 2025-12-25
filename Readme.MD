**BoxBox — F1 timing & telemetry tool (in development)**

- **Purpose:** Lightweight utilities to parse, export and inspect Formula 1 timing and telemetry datasets stored under the `cache/` folder and render quick telemetry traces in `speed_trace/`.

**Status:** In development — core scripts available in `src/`.

**Repository layout**

- `cache/` — raw per-event pickled timing & telemetry files (organized by year/event/session).
- `speed_trace/` — generated telemetry HTML traces (quick visual outputs).
- `src/` — utility scripts:
  - `get_data.py` — helpers to load and normalise cached `.ff1pkl` files.
  - `export_data.py` — export/transform routines for downstream analysis.
  - `speed_tace.py` — telemetry trace generation .

Quick Start

1. Ensure Python 3.8+ is installed.
2. (Recommended) create and activate a virtualenv:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies (`requirements.txt` to be added later on).

4. Run the data helpers (examples):

```powershell
python src\get_data.py    # load or inspect cached files
python src\export_data.py # export or transform datasets
python src\speed_tace.py  # generate telemetry traces 
```


Contributing

- Open an issue or create a PR with changes. Prefer small, focused commits and document any required dependency additions.

Contact

- For questions or pairing, leave an issue in this repo.
