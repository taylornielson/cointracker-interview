
# TODO: Decouple fetch and save
from core.services.chain_service.btc_service import ChainServiceInterface


def sync_wallet_transactions(wallet_address, sync_params, chain_service, db_service):
    sync_from = sync_params.get("sync_from", None)
    total_transactions_synced, total_transactions_saved = chain_service.sync_wallet_transactions(wallet_address, sync_from, db_service)
    return total_transactions_synced, total_transactions_saved
