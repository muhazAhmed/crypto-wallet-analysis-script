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

def compute_portfolio_volatility(wallet_data_path):
    """
    Compute Portfolio Volatility (Standard Deviation of Daily Returns) for each wallet.
    """

    # Load transaction data
    wallet_df = pd.read_csv(wallet_data_path)

    # Ensure timestamps are in datetime format
    wallet_df["timestamp"] = pd.to_datetime(wallet_df["timestamp"])

    # Sort by wallet and timestamp
    wallet_df = wallet_df.sort_values(by=["wallet_address", "timestamp"])

    # Calculate cumulative balance for each wallet over time
    wallet_df["cumulative_balance"] = wallet_df.groupby("wallet_address")["amount"].cumsum()

    # Compute daily percentage change (daily returns)
    wallet_df["daily_return"] = wallet_df.groupby("wallet_address")["cumulative_balance"].pct_change()

    # Calculate standard deviation (volatility) of daily returns per wallet
    volatility_df = wallet_df.groupby("wallet_address")["daily_return"].std().reset_index()
    volatility_df = volatility_df.rename(columns={"daily_return": "portfolio_volatility"})

    return volatility_df  # Return instead of saving directly

def compute_sharpe_ratio(wallet_df):
    """
    Compute Sharpe Ratio for each wallet.
    """

    # Ensure required columns exist
    if "roi" not in wallet_df.columns or "portfolio_volatility" not in wallet_df.columns:
        print("❌ Missing required columns for Sharpe Ratio calculation!")
        return wallet_df  # Return unchanged DataFrame

    # Risk-free rate (assumed to be 0% in crypto)
    risk_free_rate = 0

    # Compute Sharpe Ratio
    wallet_df["sharpe_ratio"] = (wallet_df["roi"] - risk_free_rate) / wallet_df["portfolio_volatility"]

    # Replace infinite/NaN values with 0 (happens when volatility is 0)
    wallet_df["sharpe_ratio"] = wallet_df["sharpe_ratio"].replace([float("inf"), float("-inf")], 0).fillna(0)

    return wallet_df  # Return updated DataFrame

def compute_loss_ratio(wallet_data_path):
    """
    Compute Historical Loss Ratio for each wallet.
    """

    # Load transaction data
    wallet_df = pd.read_csv(wallet_data_path)

    # Ensure required columns exist
    if "amount" not in wallet_df.columns or "wallet_address" not in wallet_df.columns:
        print("❌ Missing required columns for Loss Ratio calculation!")
        return pd.DataFrame()  # Return empty DataFrame if missing columns

    # Identify outgoing transactions (sell trades)
    outgoing_trades = wallet_df[wallet_df["amount"] < 0].copy()

    # Check if the sell price is lower than the buy price (loss-making trades)
    outgoing_trades["loss_trade"] = outgoing_trades["amount"] < 0  # True if amount is negative

    # Count losing trades per wallet
    loss_counts = outgoing_trades.groupby("wallet_address")["loss_trade"].sum().reset_index()
    loss_counts = loss_counts.rename(columns={"loss_trade": "losing_trades"})

    # Count total trades per wallet
    total_trades = wallet_df.groupby("wallet_address")["txHash"].count().reset_index()
    total_trades = total_trades.rename(columns={"txHash": "total_trades"})

    # Merge both counts
    loss_ratio_df = pd.merge(total_trades, loss_counts, on="wallet_address", how="left")
    loss_ratio_df["losing_trades"] = loss_ratio_df["losing_trades"].fillna(0)  # Fill NaN losses with 0

    # Compute Historical Loss Ratio
    loss_ratio_df["loss_ratio"] = (loss_ratio_df["losing_trades"] / loss_ratio_df["total_trades"]) * 100

    # Keep only relevant columns
    loss_ratio_df = loss_ratio_df[["wallet_address", "loss_ratio"]]

    return loss_ratio_df  # Return instead of saving directly

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
    volatility_df = compute_portfolio_volatility(wallet_data_path)
    loss_ratio_df = compute_loss_ratio(wallet_data_path)

    # Merge all features
    wallet_features_df = trading_df.merge(roi_df, on="wallet_address", how="outer")
    wallet_features_df = wallet_features_df.merge(activity_df, on="wallet_address", how="outer")
    wallet_features_df = wallet_features_df.merge(volatility_df, on="wallet_address", how="outer")
    wallet_features_df = wallet_features_df.merge(loss_ratio_df, on="wallet_address", how="outer")

    # Compute Sharpe Ratio
    wallet_features_df = compute_sharpe_ratio(wallet_features_df)

    # Save final dataset
    wallet_features_df.to_csv(output_path, index=False)
    print(f"✅ Wallet features computed and saved to {output_path}")
