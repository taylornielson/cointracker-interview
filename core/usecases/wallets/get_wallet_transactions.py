
def get_wallet_transactions(wallet_address, chain, page, pageSize, db_service):
    return db_service.get_transactions(wallet_address, chain, page, pageSize)