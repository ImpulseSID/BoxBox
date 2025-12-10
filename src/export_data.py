import fastf1


# 1. Point to your specific cache folder
cache_dir = 'cache'
fastf1.Cache.enable_cache(cache_dir) 

print("Loading session (using your cached files)...")
# Note: Use the same session details you used to download
session = fastf1.get_session(2025, 'Australia', 'Q') 
session.load()

print("Converting to CSV...")

# This converts the "Timing Data" and "Car Data" you see in your folder
# into a nice table format.
session.laps.to_csv('AustralianGP_Quali_Laps.csv', index=False)

print("Success! Open 'AustralianGP_Quali_Laps.csv' in Excel/VS Code.")