import requests
import pandas as pd
from time import sleep

BASE_URL = "https://ergast.com/api/f1"
years = list(range(2020, 2025))  # 2020 through 2024
all_data = []

for year in years:
    print(f"Fetching data for {year}...")
    
    # Get total number of rounds in the season
    season_url = f"{BASE_URL}/{year}.json"
    rounds_response = requests.get(season_url)
    num_rounds = int(rounds_response.json()['MRData']['total'])

    for rnd in range(1, num_rounds + 1):
        print(f"  Round {rnd}")
        race_url = f"{BASE_URL}/{year}/{rnd}/results.json"
        response = requests.get(race_url)
        sleep(0.25)  # be nice to the API

        try:
            race_data = response.json()['MRData']['RaceTable']['Races'][0]
            race_name = race_data['raceName']
            circuit = race_data['Circuit']['circuitName']

            for result in race_data['Results']:
                driver = result['Driver']
                constructor = result['Constructor']

                row = {
                    "year": year,
                    "round": rnd,
                    "race_name": race_name,
                    "circuit": circuit,
                    "driver": f"{driver['givenName']} {driver['familyName']}",
                    "driver_number": driver.get("permanentNumber"),
                    "constructor": constructor['name'],
                    "grid_position": int(result['grid']),
                    "finish_position": int(result['position']),
                    "fastest_lap_rank": result.get("FastestLap", {}).get("rank", None),
                    "status": result["status"],
                }
                all_data.append(row)

        except Exception as e:
            print(f"  Skipped round {rnd}: {e}")
            continue

# Save to CSV
df = pd.DataFrame(all_data)
df.to_csv("f1_race_results_2020_2024.csv", index=False)
print("Data saved to f1_race_results_2020_2024.csv")
