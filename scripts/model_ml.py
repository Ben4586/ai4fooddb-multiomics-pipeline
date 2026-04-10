import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Load data
df = pd.read_csv("integrated.csv", low_memory=False)

# Drop non-numeric columns
df = df.select_dtypes(include=['number'])

# Fill missing values
df.fillna(0, inplace=True)

# Dummy target (last column)
X = df.iloc[:, :-1]
y = df.iloc[:, -1]

# Train model
model = RandomForestRegressor()
model.fit(X, y)

# Feature importance
importance = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
})

importance.to_csv("feature_importance.csv", index=False)

print("[INFO] ML completed")