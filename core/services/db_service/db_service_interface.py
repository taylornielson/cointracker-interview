from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    def save_transaction(self, description, amount):
        raise NotImplementedError('Base db class has no implementation')

    @abstractmethod
    def save_transactions(self, transactions):
        raise NotImplementedError('Base db class has no implementation')

    @abstractmethod
    def get_transaction(self, transaction_id):
        raise NotImplementedError('Base db class has no implementation')
    
    @abstractmethod
    def get_transactions(self, wallet_address, chain, page, pageSize):
        raise NotImplementedError('Base db class has no implementation')
    
    @abstractmethod
    def save_wallet(self, wallet):
        raise NotImplementedError('Base db class has no implementation')

    @abstractmethod
    def get_wallets(self):
        raise NotImplementedError('Base db class has no implementation')

    @abstractmethod
    def delete_wallet(self, wallet_id):
        raise NotImplementedError('Base db class has no implementation')