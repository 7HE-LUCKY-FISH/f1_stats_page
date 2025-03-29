import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from xgboost import XGBClassifier

# Paths
DATA_PATH = os.path.join("..", "data", "f1_race_results_2020_2024.csv")
MODEL_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
ENCODER_PATH = os.path.join(MODEL_DIR, "label_encoders.pkl")

# Load data
df = pd.read_csv(DATA_PATH)
df.dropna(subset=["finish_position", "grid_position"], inplace=True)

# Only use podium positions: P1, P2, P3
df = df[df["finish_position"].isin([1, 2, 3])]

# Feature engineering
df["dnf"] = df["status"].apply(lambda x: 1 if "retired" in x.lower() or "collision" in x.lower() else 0)
df["fastest_lap_rank"] = df["fastest_lap_rank"].fillna("None")
df["had_fastest_lap"] = df["fastest_lap_rank"].apply(lambda x: 1 if x == "1" else 0)

# Encode categorical features
label_encoders = {}
for col in ["driver", "constructor", "circuit"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Features and target
features = ["driver", "constructor", "circuit", "grid_position", "had_fastest_lap", "dnf"]
X = df[features]

# Shift finish_position down by 1: P1 → 0, P2 → 1, P3 → 2
y = df["finish_position"].apply(lambda x: x - 1)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# XGBoost classifier setup
xgb = XGBClassifier(objective="multi:softmax", num_class=3, use_label_encoder=False, eval_metric="mlogloss", seed=42)

# Grid search
param_grid = {
    "max_depth": [3, 5, 7],
    "n_estimators": [100, 200],
    "learning_rate": [0.1, 0.3]
}

grid_search = GridSearchCV(xgb, param_grid, cv=5, scoring="f1_macro")
grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_

# Predict and evaluate
y_pred = best_model.predict(X_test)
print("Best Params:", grid_search.best_params_)
print("\n Classification Report (P1=0, P2=1, P3=2):")
print(classification_report(y_test, y_pred))

# Save model and encoders
joblib.dump(best_model, MODEL_PATH)
joblib.dump(label_encoders, ENCODER_PATH)
print("Tuned XGBoost podium model and encoders saved.")
