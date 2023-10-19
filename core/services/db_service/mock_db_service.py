from core.services.db_service.db_service_interface import DatabaseInterface

# TODO: JWT for user id
class MockDatabaseService(DatabaseInterface):
    _instance = None
    _transactions = {}
    _wallets = {}

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MockDatabaseService, cls).__new__(cls)
        return cls._instance


    def save_transaction(self, description, amount):
        transaction_id = len(self._transactions) + 1
        self._transactions[transaction_id] = {"description": description, "amount": amount}
        return transaction_id

    def save_transactions(self, wallet_address, transactions):
        transaction_map = {}
        for transaction in transactions:
            transaction_map[transaction.get("hash")] = transaction
        if wallet_address in self._transactions:
            self._transactions[wallet_address].update(transaction_map)
        else:
            self._transactions[wallet_address] = transaction_map
        return len(transactions)


    def get_transaction(self, transaction_id):
        return self._transactions.get(transaction_id)


    # TODO: Add current page, totalPage, and page size in response
    def get_transactions(self, wallet_address, chain, page, pageSize):
        start_index = int(pageSize) * int(page) - int(pageSize)
        end_index = int(start_index) + int(pageSize) + 1
        transactions = list(self._transactions.get(wallet_address, {}).values())[start_index:end_index]
        if len(transactions) == 0:
            return []
        return transactions
    
    def save_wallet(self, wallet):
        # Simplified example that ignores user instance
        # TODO add validation that the alias doesn't get duplicated
        if self._wallets.get(wallet['address']):
            # TODO put all error messages in a const file and better Error handling
            raise FileExistsError("Wallet with that address already exists")
        self._wallets[wallet['address']] = wallet
        return self._wallets[wallet['address']]
    
    def get_wallets(self):
        return list(self._wallets.values())

    def delete_wallet(self, wallet_id):
        if wallet_id in self._wallets:
            wallet_to_return = self._wallets[wallet_id]
            del self._wallets[wallet_id]
            return wallet_to_return
        else:
            raise FileNotFoundError(f'Wallet with id: {wallet_id} not found')
