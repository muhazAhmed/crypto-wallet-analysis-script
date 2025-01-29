import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

def train_model(data_path, output_path):
    """
    Train a Random Forest model to rank wallets based on performance metrics.
    """
    
    # Load preprocessed data
    df = pd.read_csv(data_path)

    # Separate features and target
    X = df.drop(columns=["wallet_address"])
    y = X.mean(axis=1)  # Use the mean of all features as a proxy score

    # Split into train (80%) and test (20%) sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Random Forest Model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predict rankings
    y_pred = model.predict(X_test)

    # Evaluate model performance
    mae = mean_absolute_error(y_test, y_pred)
    print(f"✅ Model trained. MAE: {mae:.4f}")

    # Predict scores for all wallets
    df["predicted_score"] = model.predict(X)

    # Rank wallets based on predicted scores (higher is better)
    df["predicted_rank"] = df["predicted_score"].rank(ascending=False, method="dense")

    # Save updated dataset with predicted ranks
    df.to_csv(output_path, index=False)
    print(f"✅ Predicted rankings saved to {output_path}")

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    data_dir = script_dir.parent / "data"
    
    input_path = data_dir / "wallet_features_clean.csv"
    output_path = data_dir / "wallet_predictions.csv"

    train_model(input_path, output_path)
