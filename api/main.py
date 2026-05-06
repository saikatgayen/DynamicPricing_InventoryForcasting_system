from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import os

# Initialize app
app = FastAPI(title="Dynamic Pricing API")

# Get the directory where main.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build absolute paths to the model and features
# This goes UP one level from 'api' then into 'model'
model_path = os.path.join(BASE_DIR, "..", "model", "xgb_model.pkl")
features_path = os.path.join(BASE_DIR, "..", "model", "features.pkl")

# Load model and features
model = joblib.load(model_path)
features = joblib.load(features_path)


# -----------------------------
# Input Schema (VERY IMPORTANT)
# -----------------------------
class PricingInput(BaseModel):
    Our_Price: float
    Competitor_Price: float
    Price_Gap: float
    Relative_Price_Index: float
    Elasticity: float
    Weekly_Sales: float
    sales_lag_1: float
    sales_lag_2: float
    sales_lag_4: float
    sales_rolling_mean_4: float
    sales_rolling_std_4: float
    Weeks_Until_Stockout: float
    Reorder_Flag: int


# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
def home():
    return {"message": "Dynamic Pricing API is running"}


# -----------------------------
# Prediction Endpoint
# -----------------------------
@app.post("/predict")
def predict(data: PricingInput):
    try:
        # Convert to DataFrame
        df = pd.DataFrame([data.dict()])

        # Ensure correct column order
        df = df[features]

        # Predict
        prediction = model.predict(df)[0]

        return {
            "optimal_price": round(float(prediction), 2)
        }

    except Exception as e:
        return {"error": str(e)}