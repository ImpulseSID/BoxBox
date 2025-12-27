import fastf1
import fastf1.plotting
import plotly.graph_objects as go
import pandas as pd
import os

# SETUP
fastf1.plotting.setup_mpl(misc_mpl_mods=False)
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(script_dir)
cache_dir = os.path.join(root_dir, 'cache')
output_dir = os.path.join(root_dir, 'dominance_maps')

fastf1.Cache.enable_cache(cache_dir)
os.makedirs(output_dir, exist_ok=True)

# --- RACE MENU ---
def select_race(year):
    try:
        schedule = fastf1.get_event_schedule(year, include_testing=False)
        if schedule.empty:
            print(f"No schedule found for {year}.")
            return None
        
        # Get list of races
        races = schedule['EventName'].tolist()
        
        print(f"\n--- {year} Formula 1 Season ---")
        for i, race in enumerate(races, start=1):
            print(f"{i:2d}. {race}")
            
        while True:
            try:
                choice = int(input("\nSelect race number: "))
                if 1 <= choice <= len(races):
                    return races[choice - 1]
            except ValueError:
                pass
            print("Invalid choice.")
    except Exception as e:
        print(f"Error fetching schedule: {e}")
        return None

def main():
    # --- USER INPUTS ---
    while True:
        try:
            year_input = input("Enter Season Year (e.g. 2024): ").strip()
            year = int(year_input)
            break
        except ValueError:
            print("Please enter a valid number.")

    race = select_race(year)
    if not race: 
        return

    # HARDCODED SESSION: Always Qualifying
    session_type = 'Q'

    print(f"\nLoading {year} {race} - Qualifying...")
    try:
        session = fastf1.get_session(year, race, session_type)
        session.load()
    except Exception as e:
        print(f"Error loading session: {e}")
        return

    # --- FIND TOP 2 FASTEST DRIVERS ---
    print("Finding fastest drivers...")
    try:
        # Get all quick laps, sort by fastest time
        all_fast_laps = session.laps.pick_quicklaps().sort_values(by='LapTime')
        
        # Keep only the single fastest lap per driver
        top_two_laps = all_fast_laps.drop_duplicates(subset=['Driver']).head(2)
        
        if len(top_two_laps) < 2:
            print("Error: Not enough data to compare two drivers.")
            return

        drivers_to_compare = top_two_laps['Driver'].tolist()
        drv_a = drivers_to_compare[0]
        drv_b = drivers_to_compare[1]
        
        print(f"Analyzing dominance: {drv_a} (Fastest) vs {drv_b} (2nd Fastest)")
        
    except Exception as e:
        print(f"Error analyzing laps: {e}")
        return

    # TEAMMATE COLOR CHECK
    try:
        color_a = fastf1.plotting.get_driver_color(drv_a, session=session)
        color_b = fastf1.plotting.get_driver_color(drv_b, session=session)
    except:
        color_a = 'green'
        color_b = 'red'

    if color_a == color_b:
        print(f"Teammate conflict detected! Changing {drv_b} to White.")
        color_b = '#FFFFFF' 
        
    driver_colors = {drv_a: color_a, drv_b: color_b}

    # --- PREPARE TELEMETRY ---
    telemetry_data = []
    for drv in drivers_to_compare:
        lap = session.laps.pick_drivers(drv).pick_fastest()
        tel = lap.get_telemetry().add_distance()
        tel['Driver'] = drv
        telemetry_data.append(tel)

    ref_tel = telemetry_data[0] 
    sec_tel = telemetry_data[1] 

    # Mini-Sectors
    chunk_size = 10 
    total_distance = max(ref_tel['Distance'])
    
    map_segments = []
    last_x = None
    last_y = None

    print(f"Calculating mini-sectors ({chunk_size}m chunks)...")
    
    for i in range(0, int(total_distance), chunk_size):
        start_dist = i
        end_dist = i + chunk_size

        mask_a = (ref_tel['Distance'] >= start_dist) & (ref_tel['Distance'] < end_dist)
        mask_b = (sec_tel['Distance'] >= start_dist) & (sec_tel['Distance'] < end_dist)

        if not mask_a.any() or not mask_b.any():
            continue

        speed_a = ref_tel.loc[mask_a, 'Speed'].mean()
        speed_b = sec_tel.loc[mask_b, 'Speed'].mean()

        if pd.isna(speed_a) or pd.isna(speed_b):
            continue

        if speed_a > speed_b:
            fastest_driver = drv_a
            chunk_color = driver_colors[drv_a]
        else:
            fastest_driver = drv_b
            chunk_color = driver_colors[drv_b]

        chunk_x = ref_tel.loc[mask_a, 'X'].tolist()
        chunk_y = ref_tel.loc[mask_a, 'Y'].tolist()

        if len(chunk_x) > 0:
            # Connect to previous segment (Gap Filling)
            if last_x is not None:
                chunk_x.insert(0, last_x)
                chunk_y.insert(0, last_y)

            last_x = chunk_x[-1]
            last_y = chunk_y[-1]

            map_segments.append({
                'x': chunk_x,
                'y': chunk_y,
                'color': chunk_color,
                'driver': fastest_driver
            })

    # --- 4. PLOTLY MAP ---
    fig = go.Figure()

    for segment in map_segments:
        fig.add_trace(go.Scatter(
            x=segment['x'],
            y=segment['y'],
            mode='lines',
            line=dict(color=segment['color'], width=6),
            hoverinfo='text',
            hovertext=f"Faster: {segment['driver']}",
            showlegend=False
        ))

    # Legend
    for drv in drivers_to_compare:
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode='lines',
            line=dict(color=driver_colors[drv], width=6),
            name=drv
        ))

    fig.update_layout(
        title=f"Track Dominance: {drv_a} vs {drv_b} ({year} {race})",
        template="plotly_dark",
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False, scaleanchor="x", scaleratio=1),
        height=800,
        margin=dict(l=0, r=0, t=50, b=0)
    )

    output_filename = f"Dominance_{drv_a}_vs_{drv_b}_{year}.html"
    output_path = os.path.join(output_dir, output_filename)
    print(f"Saving to: {output_path}")
    fig.write_html(output_path, auto_open=True)

if __name__ == "__main__":
    main()