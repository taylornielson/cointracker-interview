import time
import requests
from datetime import datetime

from core.services.chain_service.chain_service_interface import ChainServiceInterface

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5
SECONDS_TO_MILLISECOND_MULTIPLE = 1000
SATOSHIS_TO_BTC_DIVISOR = 100000000

PAGINATION_OFFSET = 50
BITCOIN_API_BASE_URL = "https://blockchain.info/rawaddr/{}"

# TODO: Look into ccxt blockchains options


#? Do we want to store partial syncs? Or do a complete success vs complete fail
# Currently doing a partial sync
class BtcService(ChainServiceInterface):

    def get_balance(self, wallet_address):
        base_url = "https://chain.api.btc.com/v3/address/"
        api_url = f"{base_url}{wallet_address}"
        response = requests.get(api_url)
        data = response.json().get('data')
        print(data)
        return {
            "address": wallet_address,
            "raw_balance": data.get('balance'),
            "normalized_balance": data.get('balance') / SATOSHIS_TO_BTC_DIVISOR
        }


    def sync_wallet_transactions(self, wallet_address, sync_from, db_service):
        total_transactions = 0
        total_transactions_fetched = 0
        total_transactions_saved = 0
        while True:  
            try:
                print("Loop")
                txn_response = self.fetch_transactions(wallet_address, sync_from, MAX_RETRIES)
                total_transactions = txn_response.get("n_tx")
                fetched_transactions = txn_response.get("txs")
                total_transactions_fetched += len(fetched_transactions)
                total_transactions_saved += db_service.save_transactions(fetched_transactions)
                sync_from += PAGINATION_OFFSET
                if total_transactions <= sync_from:
                    break
            except Exception as e:
                # Log and Continue
                print(e)
        return total_transactions_fetched, total_transactions_saved
        


    def dateStringToMillisecondsSinceEpoch(date_string):
        date_format = "%Y-%m-%d %H:%M:%S"
        parsed_date = datetime.strptime(date_string, date_format)

        timestamp_milliseconds = int(parsed_date.timestamp() * SECONDS_TO_MILLISECOND_MULTIPLE)

        return timestamp_milliseconds
    

    def fetch_transactions(wallet_address, offset, limit=PAGINATION_OFFSET, retries = 3):
        url = BITCOIN_API_BASE_URL.format(wallet_address)
        params = {
            "offset": offset
        }
        
        for _ in range(retries):
            response = requests.get(url, params=params)
            if response.status_code == 200:
                print("200")
                data = response.json()
                return data
            elif response.status_code == 429:  
                print("429")
                # Could add an expontential backoff if needed
                retry_after = int(response.headers.get("Retry-After", 1))
                print(retry_after //1000)
                time.sleep(retry_after//1000)
            else:
                raise Exception(f"Failed to fetch transactions. Status Code: {response.status_code}")
        raise Exception("Max retries reached. Could not fetch transactions.")
