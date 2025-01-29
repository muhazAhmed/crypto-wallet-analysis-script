from pathlib import Path
import pandas as pd
import requests

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
        return transaction_data  
    else:  
        print(f"Failed to fetch transaction details for {wallet_address}: {response.status_code} - {response.text}")  
        return None  


def main():  
    # Your Helius API key ID  
    api_key_id = 'b951bf96-d039-4a70-879e-90416334d353'  
    
    # Load wallet addresses from CSV without a header  
    script_dir = Path(__file__).resolve().parent
    data_file_path = script_dir.parent / 'data' / 'top_traders_account_numbers.csv'
    addresses_df = pd.read_csv(data_file_path, header=None)
    
    # Assuming wallet addresses are in the first column (index 0)
    wallet_addresses = addresses_df[0].tolist()  # This will refer to the first column by index 0
    all_transactions = []  

    # Fetch data for each wallet address  
    for wallet_address in wallet_addresses:  
        transactions = fetch_transaction_details(wallet_address, api_key_id)  

        if transactions:  
            # Append wallet address and transaction details to the results  
            for transaction in transactions:  
                transaction['wallet_address'] = wallet_address  # Include the wallet address in the transaction data  
                all_transactions.append(transaction)  

    # Ensure the directory exists before saving the file  
    output_dir = script_dir.parent / 'data'  # Set output directory
    output_dir.mkdir(parents=True, exist_ok=True)  # Create directory if it doesn't exist

    # Save fetched data to wallet_data.csv  
    if all_transactions:  
        output_df = pd.DataFrame(all_transactions)  
        output_df.to_csv(output_dir / 'wallet_data.csv', index=False)  
        print("Fetched data saved to wallet_data.csv")  

if __name__ == "__main__":  
    main()

