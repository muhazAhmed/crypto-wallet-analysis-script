from pathlib import Path
import pandas as pd
import requests
import time

def fetch_transaction_details(wallet_address, api_key_id):  
    """  
    Fetch transaction history for a given wallet address using the Helius API.  
    """  
    url = f'https://api.helius.xyz/v0/addresses/{wallet_address}/transactions?api-key={api_key_id}'  
    headers = {"accept": "application/json"}  
    response = requests.get(url, headers=headers)  

    if response.status_code == 200:  
        transaction_data = response.json()  
        return transaction_data if transaction_data else []  
    else:  
        print(f"❌ Failed to fetch transaction details for {wallet_address}: {response.status_code} - {response.text}")  
        return []  


def fetch_portfolio_data(wallet_address, api_key_id):
    """  
    Fetch portfolio (token balances) for a given wallet address using the Helius API.  
    """  
    url = f'https://api.helius.xyz/v0/addresses/{wallet_address}/balances?api-key={api_key_id}'  
    headers = {"accept": "application/json"}  
    response = requests.get(url, headers=headers)  

    if response.status_code == 200:  
        portfolio_data = response.json()
        
        # ✅ Extract only the token balances from the response
        tokens = portfolio_data.get("tokens", [])  # Get the list inside "tokens", return [] if not found
        
        # Debug: Print the extracted token list
        print(f"\n✅ Extracted tokens for {wallet_address}\n")
        
        return tokens  # Now returning a list directly
    else:  
        print(f"❌ Failed to fetch portfolio data for {wallet_address}: {response.status_code} - {response.text}")  
        return []  


def main():  
    api_key_id = 'b951bf96-d039-4a70-879e-90416334d353'  
    
    script_dir = Path(__file__).resolve().parent
    data_file_path = script_dir.parent / 'data' / 'top_traders_account_numbers.csv'

    # Debug: Confirm file path
    print(f"📂 Looking for CSV file at: {data_file_path}")
    addresses_df = pd.read_csv(data_file_path, header=None)
    
    wallet_addresses = addresses_df[0].tolist()
    all_transactions = []  
    all_portfolios = []

    for wallet_address in wallet_addresses:  
        transactions = fetch_transaction_details(wallet_address, api_key_id)  
        portfolio = fetch_portfolio_data(wallet_address, api_key_id)

        if transactions:  
            for transaction in transactions:  
                transaction['wallet_address'] = wallet_address  
                all_transactions.append(transaction)  
        
        if portfolio:
            for token in portfolio:
                token['wallet_address'] = wallet_address
                all_portfolios.append(token)

        time.sleep(1)  # Rate limiting

    output_dir = script_dir.parent / 'data'  
    output_dir.mkdir(parents=True, exist_ok=True)  

    if all_transactions:  
        print(f"✅ {len(all_transactions)} transaction records found. Saving to CSV...")
        pd.DataFrame(all_transactions).to_csv(output_dir / 'wallet_data.csv', index=False)  
        print("📂 Fetched transaction data saved to wallet_data.csv")  
    else:  
        print("❌ No transaction data found. CSV not created.")

    # Debug: Check if portfolio data exists
    if all_portfolios:
        print(f"✅ {len(all_portfolios)} portfolio records found. Saving to CSV...")
        pd.DataFrame(all_portfolios).to_csv(output_dir / 'portfolio_data.csv', index=False)
        print("📂 Fetched portfolio data saved to portfolio_data.csv")  
    else:
        print("❌ No portfolio data found. CSV not created.")

if __name__ == "__main__":  
    main()
