from flask_restx import fields
# Todo add marshmellow for validation

wallet_model = {
    'address': fields.String(required=True, description='Wallet public address'),
    'chain': fields.String(required=True, description='Blockchain type (e.g., BTC)'),
    'alias': fields.String(required=True, description='Wallet alias')
}