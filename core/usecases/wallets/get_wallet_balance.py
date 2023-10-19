
def get_wallet_balance(wallet_address, chain_service):
    return chain_service.get_balance(wallet_address)