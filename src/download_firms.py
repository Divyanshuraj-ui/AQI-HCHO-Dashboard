import pandas as pd

# Sample FIRMS-style dataset
data = {
    "latitude": [30.9, 29.8, 28.6, 25.5, 23.0],
    "longitude": [75.8, 76.5, 77.2, 85.1, 72.8],
    "brightness": [330, 350, 310, 295, 280],
    "fire_count": [45, 62, 20, 15, 8],
    "state": ["Punjab", "Haryana", "Delhi", "Bihar", "Maharashtra"],
}

df = pd.DataFrame(data)

df.to_csv("data/firms_fire_data.csv", index=False)

print("NASA FIRMS sample data saved!")
print(df.head())
