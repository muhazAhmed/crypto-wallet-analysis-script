import pandas as pd
from pathlib import Path

def compute_roi(wallet_data_path, portfolio_data_path):
    """
    Compute ROI (Return on Investment) for each wallet.
    """

    # Load transaction data
    wallet_df = pd.read_csv(wallet_data_path)
    portfolio_df = pd.read_csv(portfolio_data_path)

    # Ensure wallet_address is a string (prevents NaN issues)
    wallet_df["wallet_address"] = wallet_df["wallet_address"].astype(str)
    portfolio_df["wallet_address"] = portfolio_df["wallet_address"].astype(str)

    # Get the first transaction amount for each wallet (Initial Investment)
    initial_investment = (
        wallet_df.groupby("wallet_address")["amount"]
        .first()
        .reset_index()
        .rename(columns={"amount": "initial_investment"})
    )

    # Get the latest portfolio value per wallet (Final Portfolio Value)
    portfolio_values = (
        portfolio_df.groupby("wallet_address")["amount"]
        .sum()
        .reset_index()
        .rename(columns={"amount": "final_portfolio_value"})
    )

    # Merge data
    roi_df = pd.merge(initial_investment, portfolio_values, on="wallet_address", how="inner")

    # Compute ROI
    roi_df["roi"] = ((roi_df["final_portfolio_value"] - roi_df["initial_investment"]) / roi_df["initial_investment"]) * 100

    return roi_df  # Return instead of saving directly


def compute_trading_frequency(wallet_data_path):
    """
    Compute Trading Frequency for each wallet.
    """

    # Load transaction data
    wallet_df = pd.read_csv(wallet_data_path)

    # Ensure timestamps are in datetime format
    wallet_df["timestamp"] = pd.to_datetime(wallet_df["timestamp"])

    # Count total transactions per wallet
    transaction_counts = wallet_df.groupby("wallet_address")["txHash"].count().reset_index()
    transaction_counts = transaction_counts.rename(columns={"txHash": "total_transactions"})

    # Find the first and last transaction date per wallet
    activity_period = wallet_df.groupby("wallet_address")["timestamp"].agg(["min", "max"]).reset_index()
    activity_period["days_active"] = (activity_period["max"] - activity_period["min"]).dt.days + 1  # Ensure at least 1 day

    # Merge data
    trading_freq_df = pd.merge(transaction_counts, activity_period, on="wallet_address", how="inner")

    # Compute trading frequency
    trading_freq_df["trading_frequency"] = trading_freq_df["total_transactions"] / trading_freq_df["days_active"]

    # Drop unnecessary columns
    trading_freq_df = trading_freq_df[["wallet_address", "total_transactions", "days_active", "trading_frequency"]]

    return trading_freq_df  # Return instead of saving directly

def compute_activity_score(wallet_data_path):
    """
    Compute Activity Score for each wallet.
    """

    # Load transaction data
    wallet_df = pd.read_csv(wallet_data_path)

    # Ensure timestamps are in datetime format
    wallet_df["timestamp"] = pd.to_datetime(wallet_df["timestamp"])

    # Count total transactions per wallet
    transaction_counts = wallet_df.groupby("wallet_address")["txHash"].count().reset_index()
    transaction_counts = transaction_counts.rename(columns={"txHash": "total_transactions"})

    # Find the first and last transaction date per wallet
    activity_period = wallet_df.groupby("wallet_address")["timestamp"].agg(["min", "max"]).reset_index()
    activity_period["days_active"] = (activity_period["max"] - activity_period["min"]).dt.days + 1  # Ensure at least 1 day

    # Merge data
    activity_score_df = pd.merge(transaction_counts, activity_period, on="wallet_address", how="inner")

    # Compute Activity Score
    activity_score_df["activity_score"] = activity_score_df["total_transactions"] / activity_score_df["days_active"]

    # Keep only necessary columns
    activity_score_df = activity_score_df[["wallet_address", "activity_score"]]

    return activity_score_df  # Return instead of saving directly

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    data_dir = script_dir.parent / "data"

    wallet_data_path = data_dir / "wallet_data.csv"
    portfolio_data_path = data_dir / "portfolio_data.csv"
    output_path = data_dir / "wallet_features.csv"

    # Compute features
    trading_df = compute_trading_frequency(wallet_data_path)
    roi_df = compute_roi(wallet_data_path, portfolio_data_path)
    activity_df = compute_activity_score(wallet_data_path)

    # Merge all features
    wallet_features_df = trading_df.merge(roi_df, on="wallet_address", how="outer")
    wallet_features_df = wallet_features_df.merge(activity_df, on="wallet_address", how="outer")

    # Save final dataset
    wallet_features_df.to_csv(output_path, index=False)
    print(f"✅ Wallet features computed and saved to {output_path}")
