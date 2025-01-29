import pandas as pd

def format_transaction_data(transactions, wallet_address):
    """  
    Clean and structure transaction data, flatten token transfers.
    """  
    formatted_transactions = []
    for tx in transactions:
        token_transfers = tx.get("tokenTransfers", [])  # List of token transfers
        sol_amount = tx.get("lamports", 0) / 1e9

        if not token_transfers:  # If no token transfers, save as a single row
            formatted_transactions.append({
                "wallet_address": wallet_address,
                "txHash": tx.get("signature", ""),  
                "timestamp": pd.to_datetime(tx.get("timestamp", 0), unit='s'),  
                "amount": round(sol_amount, 9),  
                "fromUser": None,
                "toUser": None,
                "tokenAmount": None,
                "mint": None,
                "fee": f"{tx.get('fee', 0) / 1e9:.9f}",  
            })
        else:
            for transfer in token_transfers:
                token_amount = transfer.get("tokenAmount", 0)
                formatted_transactions.append({
                    "wallet_address": wallet_address,
                    "txHash": tx.get("signature", ""),
                    "timestamp": pd.to_datetime(tx.get("timestamp", 0), unit='s'),
                    "amount": round(sol_amount, 9) if sol_amount > 0 else round(token_amount, 9),   
                    "fromUser": transfer.get("fromUserAccount"),
                    "toUser": transfer.get("toUserAccount"),
                    "tokenAmount": transfer.get("tokenAmount"),
                    "mint": transfer.get("mint"),
                    "fee": f"{tx.get('fee', 0) / 1e9:.9f}",
                })
    return formatted_transactions


def format_portfolio_data(portfolio, wallet_address):
    """  
    Convert token balances into human-readable amounts and ensure wallet_address is included.
    """  
    formatted_portfolio = []

    # Process Fungible Tokens
    for token in portfolio.get("tokens", []):
        formatted_portfolio.append({
            "wallet_address": wallet_address,
            "asset_type": "Token",  # New column to differentiate tokens vs NFTs
            "token_account": token.get("tokenAccount"),
            "mint": token.get("mint"),
            "amount": round(token.get("amount", 0) / (10 ** token.get("decimals", 0)), 9),  
            "decimals": token.get("decimals", 0),
            "symbol": None,  # Tokens may not have symbols in response
            "nft_name": None,  # Only NFTs will have names
            "nft_image": None,  # Only NFTs will have image URLs
        })

    # Process NFT Holdings
    for nft in portfolio.get("nfts", []):
        formatted_portfolio.append({
            "wallet_address": wallet_address,
            "asset_type": "NFT",  # Mark NFTs separately
            "token_account": nft.get("tokenAccount"),
            "mint": nft.get("mint"),
            "amount": 1,  # NFTs always have "1" since they're non-fungible
            "decimals": 0,
            "symbol": nft.get("symbol"),  # NFT Symbol (if available)
            "nft_name": nft.get("name"),  # NFT Name
            "nft_image": nft.get("imageUrl"),  # NFT Image URL
        })

    return formatted_portfolio
