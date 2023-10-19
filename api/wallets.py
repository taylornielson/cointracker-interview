from flask import request
from flask_restx import Resource, Namespace, fields
from core.services.chain_service.btc_backup_service import BtcBackupService
from core.services.chain_service.btc_service import BtcService
from core.services.db_service.mock_db_service import MockDatabaseService
from werkzeug.exceptions import BadRequest
from core.usecases.wallets.add_wallet_address import add_new_wallet
from core.usecases.wallets.get_all_wallets import get_all_wallets
from core.usecases.wallets.delete_wallet import delete_wallet
from core.usecases.wallets.get_wallet_balance import get_wallet_balance
from core.usecases.wallets.get_wallet_transactions import get_wallet_transactions
from core.usecases.wallets.sync_wallet_transactions import sync_wallet_transactions
from core.util.id_utils import generate_uuid4 as uuid
api = Namespace('wallets', description='Cryptocurrency Wallet Operations')

# TODO Break the models into their own directory
add_wallet_request = api.model('AddWalletRequest', {
    'address': fields.String(required=True, description='public address'),
    'chain': fields.String(required=True, description='the blockchain the address belongs to'),
    'alias': fields.String(required=False, description='an alias to distinguish the wallet, defaults to a generated uuid4')},
)

# Can add other sync params, like types of transactions, asc/desc, limit, etc.
sync_wallet_request = api.model('SyncWalletRequest', {
    'sync_from': fields.String(required=False, description='timestamp in to sync from', default="0"),
    'chain': fields.String(required=True, description='the blockchain the address belongs to')}
)



# TODO: Add Authentication so user can only add/access theirs + correct organization in db
@api.route('/')
class AddressResource(Resource):
    @api.expect(add_wallet_request)
    def post(self):
        try:
            # TODO: Add Validation
            db_service = MockDatabaseService()
            saved_wallet = add_new_wallet(api.payload, db_service)
            return {'message': 'created', 'data': saved_wallet}, 201
        except Exception as e:
            raise BadRequest(description=str(e))    
    def get(self): 
        try:
            db_service = MockDatabaseService()
            wallets = get_all_wallets(db_service)
            return {'message': 'Success', 'data': wallets}, 200
        except Exception as e:
            raise BadRequest(description=str(e))     


@api.route('/<string:wallet_address>')
class SpecificAddressResource(Resource):
    def delete(self, wallet_address):
        try:
            # TODO: Add Validation
            db_service = MockDatabaseService()
            deleted_wallet = delete_wallet(wallet_address, db_service)
            return {'message': 'deleted', 'data': deleted_wallet}, 201
        except Exception as e:
            raise BadRequest(description=str(e))   
    # TODO: add a Get to get a specific wallet by address


# TODO: Make this kick off an async process and return
@api.route('/<string:wallet_address>/sync')
class SpecificAddressSyncResource(Resource):
    @api.expect(sync_wallet_request)
    def post(self, wallet_address):
        try:
            db_service = MockDatabaseService()
            # TODO: make the chain service be based on the chain type
            chain_service = BtcBackupService()
            sync_params = api.payload
            synced_transaction_count, saved_transaction_count = sync_wallet_transactions(wallet_address, sync_params, chain_service, db_service)
            if synced_transaction_count == saved_transaction_count:
                return {'message': 'full success', 'data': synced_transaction_count}, 201
            else:
                return {'message': 'partial success', 'data': f'fetched {synced_transaction_count}, saved: {saved_transaction_count}'}, 201 
        except Exception as e:
            raise BadRequest(description=str(e))   


# TODO: we could do a summary endpoint that returns balance and last n number of transactions


@api.route('/<string:wallet_address>/<string:chain>/balance')
class SpecificAddressSyncResource(Resource):
    def get(self, wallet_address, chain):
        try:
            # TODO: make the chain service be based on the chain type
            chain_service = BtcService()
            # TODO add ticker based on chain? (for native)
            balance_response = get_wallet_balance(wallet_address, chain_service)
            return {'message': 'success', 'data': balance_response}, 201 
        except Exception as e:
            raise BadRequest(description=str(e))    


# TODO: Move page and pageSize to consts
@api.route('/<string:wallet_address>/<string:chain>/transactions')
class SpecificAddressTransactionsResource(Resource):
    def get(self, wallet_address, chain):
        try:
            page = max(int(request.args.get('page', 1)), 1)
            pageSize = request.args.get('pageSize', 50)
            # TODO: make the chain service be based on the chain type
            db_service = MockDatabaseService()
            transactions = get_wallet_transactions(wallet_address, chain, page, pageSize, db_service)
            return {'message': 'success', 'data': transactions}, 201 
        except Exception as e:
            raise BadRequest(description=str(e))    
