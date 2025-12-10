import fastf1
import os

# --- 1. SETUP CACHE ---
script_dir = os.path.dirname(os.path.abspath(__file__))   # get the script directory
cache_dir = os.path.join(os.path.dirname(script_dir), 'cache')   # cerate the cache in root
os.makedirs(cache_dir, exist_ok=True)  # check if cache directory exists
fastf1.Cache.enable_cache(cache_dir)   # enable cache

# --- 2. CONFIGURATION ---
TARGET_YEAR = 2025  # Can be 2024, 2023, ....

def main():
    print(f"Fetching schedule for {TARGET_YEAR}...\n")
    
    # Get the schedule for the whole year
    # include_testing=False hides pre-season testing (Round 0)
    schedule = fastf1.get_event_schedule(TARGET_YEAR, include_testing=False)

    # --- 3. SELECT A RACE ---
    print(f"--- {TARGET_YEAR} Formula 1 Season ---")
    
    # Iterate through the schedule to print a menu
    # 'RoundNumber' is 1 for Australia, 2 for China, etc.
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

    # --- 4. SELECT A SESSION ---
    # FastF1 uses specific codes: 'FP1', 'Q', 'R', etc.
    
    # Determine if it is a Sprint Weekend to show correct options
    # (FastF1 events have a format property, but for simplicity, we list common options)
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
    
    session_choice = input("\nEnter Session Code (e.g. Q or R): ").upper().strip()

    if session_choice not in session_options:
        print(f"Warning: '{session_choice}' might not be valid, but trying anyway...")

    # --- 5. LOAD THE DATA ---
    print(f"\nLoading data for {event.EventName} - {session_options.get(session_choice, session_choice)}...")
    
    try:
        # We pass the event object and the session code
        session = fastf1.get_session(TARGET_YEAR, round_choice, session_choice)
        session.load()
        
        print("\nSUCCESS! Session Loaded.")
        print(f"Fastest Lap: {session.laps.pick_fastest()['LapTime']}")
        
    except Exception as e:
        print(f"\nError loading session: {e}")
        print("Note: If you selected a future race, data won't exist yet!")

if __name__ == "__main__":
    main()