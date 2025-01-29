import pandas as pd
from pathlib import Path

def rank_wallets(wallet_features_path, output_path):
    """
    Rank wallets based on weighted scoring of different metrics.
    """

    # Load wallet features
    df = pd.read_csv(wallet_features_path)

    # Ensure numeric columns are converted properly (handle NaNs)
    for col in ["roi", "trading_frequency", "sharpe_ratio", "loss_ratio"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Define weightage for scoring
    weights = {
        "roi": 0.4,                # Higher ROI is better
        "trading_frequency": 0.3,  # More frequent trades = better
        "sharpe_ratio": 0.2,       # Higher risk-adjusted return is better
        "loss_ratio": -0.1         # Lower loss ratio is better
    }

    # Compute weighted score
    df["score"] = (
        (df["roi"] * weights["roi"]) +
        (df["trading_frequency"] * weights["trading_frequency"]) +
        (df["sharpe_ratio"] * weights["sharpe_ratio"]) +
        (df["loss_ratio"] * weights["loss_ratio"])  # Negative weight for losses
    )

    # Rank wallets (higher score = better rank)
    df = df.sort_values(by="score", ascending=False)
    df["rank"] = range(1, len(df) + 1)

    # Save rankings
    df.to_csv(output_path, index=False)
    print(f"✅ Wallet rankings saved to {output_path}")

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    data_dir = script_dir.parent / "data"

    wallet_features_path = data_dir / "wallet_features.csv"
    output_path = data_dir / "wallet_rankings.csv"

    rank_wallets(wallet_features_path, output_path)
