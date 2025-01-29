import pandas as pd
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler

def preprocess_wallet_features(wallet_features_path, output_path):
    """
    Preprocess wallet features for ML by handling missing values and normalizing features.
    """
    
    # Load data
    df = pd.read_csv(wallet_features_path)
    
    # Drop non-numeric columns (wallet_address)
    wallet_ids = df["wallet_address"]
    df = df.drop(columns=["wallet_address"])

    # Handle missing values (fill NaN with median)
    df = df.fillna(df.median())

    # Normalize numerical features (Min-Max Scaling)
    scaler = MinMaxScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

    # Add wallet addresses back
    df_scaled.insert(0, "wallet_address", wallet_ids)

    # Save cleaned dataset
    df_scaled.to_csv(output_path, index=False)
    print(f"✅ Preprocessed data saved to {output_path}")

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    data_dir = script_dir.parent / "data"
    
    input_path = data_dir / "wallet_features.csv"
    output_path = data_dir / "wallet_features_clean.csv"

    preprocess_wallet_features(input_path, output_path)
