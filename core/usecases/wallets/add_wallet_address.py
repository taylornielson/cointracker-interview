
def add_new_wallet(wallet, db_service):
    return db_service.save_wallet(wallet)