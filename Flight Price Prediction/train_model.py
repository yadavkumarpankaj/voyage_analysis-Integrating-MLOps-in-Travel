"""
Script to train and save the Random Forest model and scaler for the Flask app
"""
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

print("🚀 Training Flight Price Prediction Model...")
print("=" * 50)

# Load Data
print("\n📊 Loading data...")
df = pd.read_csv("dags/data/flights.csv")
print(f"   Loaded {len(df)} records")

# Convert date to datetime
df['date'] = pd.to_datetime(df['date'])

# Extract date features
df['week_day'] = df['date'].dt.weekday
df['month'] = df['date'].dt.month
df['week_no'] = df['date'].dt.isocalendar().week
df['year'] = df['date'].dt.year
df['day'] = df['date'].dt.day

# Rename column
df.rename(columns={"to": "destination"}, inplace=True)

# Create flight speed feature
df['flight_speed'] = round(df['distance'] / df['time'], 2)

# One-hot encode categorical variables
print("\n🔄 Encoding categorical variables...")
df = pd.get_dummies(df, columns=['from', 'destination', 'flightType', 'agency'])

# Drop irrelevant features
df.drop(columns=['time', 'flight_speed', 'distance', 'date'], axis=1, inplace=True)

# Rename columns with spaces to match expected format
df.columns = df.columns.str.replace(' ', '_')
df.columns = df.columns.str.replace('(', '')
df.columns = df.columns.str.replace(')', '')

# Separate features and target
X = df.drop('price', axis=1)
Y = df['price']

# Feature order matching the Flask app
feature_order = [
    "from_Florianopolis_SC", "from_Sao_Paulo_SP", "from_Salvador_BH", "from_Brasilia_DF", 
    "from_Rio_de_Janeiro_RJ", "from_Campo_Grande_MS", "from_Aracaju_SE", "from_Natal_RN", "from_Recife_PE",
    "destination_Florianopolis_SC", "destination_Sao_Paulo_SP", "destination_Salvador_BH", 
    "destination_Brasilia_DF", "destination_Rio_de_Janeiro_RJ", "destination_Campo_Grande_MS",
    "destination_Aracaju_SE", "destination_Natal_RN", "destination_Recife_PE",
    "flightType_economic", "flightType_firstClass", "flightType_premium",
    "agency_Rainbow", "agency_CloudFy", "agency_FlyingDrops",
    "month", "year", "day"
]

# Reorder columns to match feature_order (add missing columns with zeros if needed)
for col in feature_order:
    if col not in X.columns:
        X[col] = 0

# Select and reorder columns
X = X[feature_order]

print(f"\n📐 Feature shape: {X.shape}")
print(f"   Target shape: {Y.shape}")

# Split data
print("\n✂️  Splitting data...")
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.20, random_state=42)
print(f"   Train: {X_train.shape[0]} samples")
print(f"   Test: {X_test.shape[0]} samples")

# Standardize data
print("\n📏 Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
print("\n🌲 Training Random Forest model...")
rf_model = RandomForestRegressor(
    n_estimators=300,
    max_depth=15,
    min_samples_split=10,
    max_features='sqrt',
    random_state=42,
    n_jobs=-1
)
rf_model.fit(X_train_scaled, Y_train)

# Make predictions
Y_train_pred = rf_model.predict(X_train_scaled)
Y_test_pred = rf_model.predict(X_test_scaled)

# Evaluate model
print("\n📈 Model Evaluation:")
mse = mean_squared_error(Y_test, Y_test_pred)
mae = mean_absolute_error(Y_test, Y_test_pred)
rmse = np.sqrt(mse)
r2 = r2_score(Y_test, Y_test_pred)

print(f"   Mean Absolute Error (MAE): {mae:.2f}")
print(f"   Mean Squared Error (MSE): {mse:.2f}")
print(f"   Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"   R² Score: {r2:.4f}")

# Save model and scaler
print("\n💾 Saving model files...")
with open("rf_model.pkl", "wb") as f:
    pickle.dump(rf_model, f)
print("   ✓ Saved: rf_model.pkl")

with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)
print("   ✓ Saved: scaler.pkl")

print("\n✅ Model training completed successfully!")
print("=" * 50)
print("\n📝 Next steps:")
print("   1. Run Flask app: python app.py")
print("   2. Access at: http://localhost:5000")

