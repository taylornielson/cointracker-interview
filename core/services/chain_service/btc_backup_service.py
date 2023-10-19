import time
import requests
from datetime import datetime

from core.services.chain_service.chain_service_interface import ChainServiceInterface

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5
SECONDS_TO_MILLISECOND_MULTIPLE = 1000
SATOSHIS_TO_BTC_DIVISOR = 100000000
PAGINATION_OFFSET = 50

BITCOIN_API_BASE_URL = "https://chain.api.btc.com/v3/address/{}/tx"
# TODO: Look into ccxt blockchains options


#? Do we want to store partial syncs? Or do a complete success vs complete fail
# Currently doing a partial sync
class BtcBackupService(ChainServiceInterface):

    def get_balance(self, wallet_address):
        base_url = "https://chain.api.btc.com/v3/address/"
        api_url = f"{base_url}{wallet_address}"
        response = requests.get(api_url)
        data = response.json().get('data')
        # TODO: Use validated response models
        return {
            "address": wallet_address,
            "raw_balance": data.get('balance'),
            "normalized_balance": data.get('balance') / SATOSHIS_TO_BTC_DIVISOR
        }


    def sync_wallet_transactions(self, wallet_address, sync_from, db_service):
        page_total = 0
        total_transactions_fetched = 0
        total_transactions_saved = 0
        starting_page = int(sync_from) // PAGINATION_OFFSET
        #! Currently requires a sync from where sync_from % 50 = 0, need to update this
        while True:  
            try:
                # This print is just for the demo for a visual during long syncs
                print(starting_page, page_total)
                txn_response = self.fetch_transactions(wallet_address, starting_page)
                page_total = txn_response.get('page_total')
                fetched_transactions = txn_response.get("list")
                total_transactions_fetched += len(fetched_transactions)
                total_transactions_saved += db_service.save_transactions(wallet_address, fetched_transactions)
                starting_page += 1
                if starting_page > page_total:
                    break
            except Exception as e:
                # Log and Continue
                print(e)
        return total_transactions_fetched, total_transactions_saved
        

    def fetch_transactions(self, wallet_address, page, pagesize=PAGINATION_OFFSET, retries = 3):
        url = BITCOIN_API_BASE_URL.format(wallet_address)
        params = {
            "page": page,
            "pagesize": pagesize
        }
        
        for _ in range(retries):
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json().get("data")
                return data
            elif response.status_code == 429:  
                print("retry")
                # Could add an expontential backoff if needed
                retry_after = int(response.headers.get("Retry-After", 1))
                time.sleep(retry_after)
            else:
                raise Exception(f"Failed to fetch transactions. Status Code: {response.status_code}")
        raise Exception("Max retries reached. Could not fetch transactions.")
