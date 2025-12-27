import fastf1

cache_dir = 'cache'
fastf1.Cache.enable_cache(cache_dir) 

print("Loading session ...")

# User Inputs
season = int(input("Enter year: "))
race = input("Enter race name: ")
session_type = input("Enter session type: ")

session = fastf1.get_session(season, race, session_type)
session.load()

session.laps.to_csv(f'{race}_{session_type}_Laps.csv', index=False)
