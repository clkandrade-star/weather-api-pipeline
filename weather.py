import requests
import time
import pandas as pd
from pathlib import Path

api_key = "564d9bdfe08640d885505954260605"

api_url = "https://api.weatherapi.com/v1/forecast.json"

zip_codes = [
    "90045",  # Los Angeles, CA
    "10001",  # New York, NY
    "60601",  # Chicago, IL
    "98101",  # Seattle, WA
    "33101",  # Miami, FL
    "77001",  # Houston, TX
    "85001",  # Phoenix, AZ
    "19101",  # Philadelphia, PA
    "78201",  # San Antonio, TX
    "75201",  # Dallas, TX
    "95101",  # San Jose, CA
    "78701",  # Austin, TX
    "30301",  # Atlanta, GA
    "37201",  # Nashville, TN
    "28201",  # Charlotte, NC
    "80201",  # Denver, CO
    "89101",  # Las Vegas, NV
    "97201",  # Portland, OR
    "63101",  # St. Louis, MO
    "55401",  # Minneapolis, MN
]

results = []

for zip_code in zip_codes:
    params = {
        "key": api_key,
        "q": zip_code,
        "days": 7,
    }
    response = requests.get(api_url, params=params)
    data = response.json()

    city = data["location"]["name"]
    region = data["location"]["region"]

    print(f"{city}, {region}:")
    for day in data["forecast"]["forecastday"]:
        date = day["date"]
        max_temp = day["day"]["maxtemp_f"]
        min_temp = day["day"]["mintemp_f"]
        condition = day["day"]["condition"]["text"]

        results.append({
            "zip_code": zip_code,
            "city": city,
            "region": region,
            "date": date,
            "max_temp_f": max_temp,
            "min_temp_f": min_temp,
            "condition": condition,
        })

        print(f"  {date}: {min_temp}–{max_temp}°F, {condition}")
    time.sleep(1)

df = pd.DataFrame(results)
print(df)
print(f"\nShape: {df.shape[0]} rows x {df.shape[1]} columns")

output_path = Path(__file__).parent / "weather_data.csv"
df.to_csv(output_path, index=False)
print(f"Saved to {output_path}")