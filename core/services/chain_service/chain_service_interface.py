from abc import ABC, abstractmethod

# Imagine if we had to switch from blockchair to etherscan, etc
class ChainServiceInterface(ABC):
    @abstractmethod
    def sync_wallet_transactions(self, wallet_address, sync_from, db_service):
        raise NotImplementedError('Base db class has no implementation')