import fastf1
import fastf1.plotting
import plotly.graph_objects as go
import pandas as pd
import os

# SETUP
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(script_dir)
cache_dir = os.path.join(root_dir, 'cache')
output_dir = os.path.join(root_dir, 'speed_trace')

fastf1.Cache.enable_cache(cache_dir)
os.makedirs(output_dir, exist_ok=True)

def main():
    year = 2024
    race = 'Australia'
    session_type = 'R'

    print(f"Loading {year} {race}...")
    session = fastf1.get_session(year, race, session_type)
    session.load()
    
    # Driver Styles
    team_counts = {} 
    driver_styles = {} 
    
    for drv in session.drivers:
        try:
            info = session.laps.pick_drivers(drv).iloc[0]
            team = info["Team"]
            color = fastf1.plotting.get_team_color(team, session=session)

            if team not in team_counts:
                team_counts[team] = 1
                dash = "solid"
            else:
                team_counts[team] += 1
                dash = "dash"

            driver_styles[drv] = {
                "name": info["Driver"],
                "color": color,
                "dash": dash
            }
        except:
            continue
    
    max_laps = int(session.laps["LapNumber"].max())
    fig = go.Figure()

    # Keep track of which traces belong to which lap
    lap_trace_map = {}

    trace_index = 0

    # Build Traces
    for lap in range(1, max_laps + 1):
        lap_trace_map[lap] = []

        lap_data = session.laps.pick_laps([lap])

        for drv in driver_styles:
            try:
                drv_lap = lap_data.pick_drivers(drv)
                if drv_lap.empty:
                    continue

                car = drv_lap.iloc[0].get_car_data().add_distance()
                style = driver_styles[drv]

                fig.add_trace(go.Scatter(
                    x=car["Distance"],
                    y=car["Speed"],
                    mode="lines",
                    name=style["name"],
                    line=dict(
                        color=style["color"],
                        dash=style["dash"],
                        width=2
                    ),
                    visible=(lap == 1),  # ONLY LAP 1 VISIBLE INITIALLY
                    hovertemplate=(
                        f"<b>{style['name']}</b><br>"
                        "Speed: %{y} km/h<br>"
                        "Dist: %{x} m<extra></extra>"
                    )
                ))

                lap_trace_map[lap].append(trace_index)
                trace_index += 1

            except:
                continue

    total_traces = trace_index

    # Slider Steps
    steps = []

    for lap in range(1, max_laps + 1):
        visible = [False] * total_traces
        for idx in lap_trace_map[lap]:
            visible[idx] = True

        steps.append({
            "label": str(lap),
            "method": "update",
            "args": [
                {"visible": visible},
                {"title": {"text": f"Interactive Telemetry: {year} {race} | Lap {lap}"}}
            ]
        })

    # Layout
    fig.update_layout(
        title=f"Interactive Telemetry: {year} {race} | Lap 1",
        template="plotly_dark",
        xaxis_title="Distance (m)",
        yaxis_title="Speed (km/h)",
        hovermode="x unified",
        updatemenus=[],
        sliders=[{
            "active": 0,
            "currentvalue": {
                "prefix": "Lap: ",
                "font": {"size": 18}
            },
            "pad": {"t": 50},
            "steps": steps
        }]
    )

    # Save
    output_path = os.path.join(
        output_dir,
        f"telemetry_{year}_{race.replace(' ', '_')}.html"
    )

    print(f"Saving to: {output_path}")
    fig.write_html(output_path, auto_open=True)

if __name__ == "__main__":
    main()