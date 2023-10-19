from flask_restx import Api

from .wallets import api as v1_wallets

api = Api(
    title='Wallet Management and Sync API',
    version='1.0',
    description='Manage your Wallet Addresses and Sync Transactions',
)

api.add_namespace(v1_wallets, path='/api/v1/wallets')
