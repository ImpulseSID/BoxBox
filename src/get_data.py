import fastf1
import os

# --- SETUP CACHE ---
script_dir = os.path.dirname(os.path.abspath(__file__))   # get the script directory
cache_dir = os.path.join(os.path.dirname(script_dir), 'cache')   # cerate the cache in root
os.makedirs(cache_dir, exist_ok=True)  # check if cache directory exists
fastf1.Cache.enable_cache(cache_dir)   # enable cache

# --- CONFIGURATION ---


def main():
    # --- GET YEAR FROM USER ---
    while True:
        try:
            year_input = input("Enter the Season Year: ").strip()
            target_year = int(year_input)
            
            if target_year < 2018:
                print("Warning: Prior to 2018 limited telemetry data")
            break
        except ValueError:
            print("Invalid input. Please enter a valid number")
            
    print(f"\nFetching schedule for {target_year}...\n")

    # Get the schedule for the whole year
    try:
        schedule = fastf1.get_event_schedule(target_year, include_testing=False)
        
        if schedule.empty:
            print(f"No data found for year {target_year}. Exiting.")
            return

    except Exception as e:
        print(f"Error fetching schedule: {e}")
        return


    # --- SELECT A RACE ---
    print(f"--- {target_year} Formula 1 Season ---")
    
    # Print a Menu
    for index, row in schedule.iterrows():
        print(f"{row['RoundNumber']}: {row['EventName']} ({row['Location']})")

    print("-------------------------------")
    try:
        round_choice = int(input("Enter the Round Number (e.g., 1): "))
        
        # Get the specific event object for that round
        event = schedule.get_event_by_round(round_choice)
        print(f"\nSelected: {event.EventName}")

    except (ValueError, KeyError):
        print("Invalid selection. Exiting.")
        return

    # --- SELECT A SESSION ---
    session_options = {
        'FP1': 'Free Practice 1',
        'FP2': 'Free Practice 2',
        'FP3': 'Free Practice 3',
        'Q':   'Qualifying',
        'SS':  'Sprint Qualifying (Shootout)',
        'S':   'Sprint',
        'R':   'Race'
    }

    print(f"\n--- Available Sessions for {event.EventName} ---")
    for code, name in session_options.items():
        print(f"[{code}] : {name}")
    
    print("\nTip: Enter 'ALL' for everything, or separate by comma (e.g. 'Q, R')")
    user_input = input("Enter Session Code(s): ").upper().strip()

    # Determine which codes to load
    sessions_to_load = []
    
    if user_input == 'ALL':
        sessions_to_load = list(session_options.keys())
    else:
        parts = user_input.split(',') # split the sessions by commas
        for part in parts:
            clean_code = part.strip()
            if clean_code in session_options:
                sessions_to_load.append(clean_code)
            elif clean_code:
                print(f"Warning: '{clean_code}' is not a valid code. Ignoring.")

    if not sessions_to_load:
        print("No valid sessions selected. Exiting.")
        return

    # --- LOAD THE DATA ---
    print(f"\nQueueing download for: {', '.join(sessions_to_load)}")

    for seq_code in sessions_to_load:
        full_name = session_options.get(seq_code, seq_code)
        print(f"\n--- Processing {full_name} ({seq_code}) ---")

        try:
            #Get the session object
            session = fastf1.get_session(target_year, round_choice, seq_code)
            
            # Load the data
            session.load()
            
            print(f"SUCCESS: {full_name} loaded.")
            
            # Quick Check
            if not session.laps.empty:
                fastest = session.laps.pick_fastest()
                print(f"   Fastest Lap: {fastest['LapTime']} by {fastest['Driver']}")
            else:
                print("Session loaded but contains no lap data yet")

        except Exception:
            # This handles cases where you ask for 'FP3' on a Sprint weekend (it doesn't exist)
            print("Skipped: Session not available for this event.")

if __name__ == "__main__":
    main()