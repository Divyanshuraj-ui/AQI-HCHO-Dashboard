import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

# Load Data
df = pd.read_csv("data/india_aqi.csv")

# Features
X = df[["pm25", "pm10", "no2", "co", "temperature", "humidity"]]

# Target
y = df["aqi"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestRegressor(n_estimators=200, random_state=42)

model.fit(X_train, y_train)

# Prediction
pred = model.predict(X_test)

# Metrics
r2 = r2_score(y_test, pred)
mae = mean_absolute_error(y_test, pred)

print("\n===== MODEL RESULTS =====")
print("R2 Score :", round(r2, 3))
print("MAE      :", round(mae, 2))

# Save
joblib.dump(model, "models/aqi_model.pkl")

print("\nModel Saved Successfully!")
