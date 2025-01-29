from pathlib import Path
import pandas as pd
import requests
import time  # Added for rate limiting

def fetch_transaction_details(wallet_address, api_key_id):  
    """  
    Fetch transaction details for a given wallet address using the Helius API.  
    """  
    url = f'https://api.helius.xyz/v0/addresses/{wallet_address}/transactions?api-key={api_key_id}'  
    
    headers = {  
        'accept': 'application/json'  
    }  

    response = requests.get(url, headers=headers)  

    if response.status_code == 200:  
        transaction_data = response.json()  
        return transaction_data if transaction_data else []  # Return empty list instead of None
    else:  
        print(f"Failed to fetch transaction details for {wallet_address}: {response.status_code} - {response.text}")  
        return []  # Return empty list if API call fails


def main():  
    api_key_id = 'b951bf96-d039-4a70-879e-90416334d353'  
    
    script_dir = Path(__file__).resolve().parent
    data_file_path = script_dir.parent / 'data' / 'top_traders_account_numbers.csv'
    addresses_df = pd.read_csv(data_file_path, header=None)
    
    wallet_addresses = addresses_df[0].tolist()
    all_transactions = []  

    for wallet_address in wallet_addresses:  
        transactions = fetch_transaction_details(wallet_address, api_key_id)  

        if transactions:  
            for transaction in transactions:  
                transaction['wallet_address'] = wallet_address  
                all_transactions.append(transaction)  
        
        time.sleep(1)  # Rate limiting (Wait 1 second between API calls)

    output_dir = script_dir.parent / 'data'  
    output_dir.mkdir(parents=True, exist_ok=True)  

    if all_transactions:  
        output_df = pd.DataFrame(all_transactions)  
        output_df.to_csv(output_dir / 'wallet_data.csv', index=False)  
        print("Fetched data saved to wallet_data.csv")  
    else:
        print("No transaction data found for any wallets.")

if __name__ == "__main__":  
    main()
