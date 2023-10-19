# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# from core.services.db_service.db_service_interface import DatabaseInterface

# # TODO Get DB_URL from config

# class SqlDatabaseService(DatabaseInterface):
#     _instance = None

#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(SqlDbService, cls).__new__(cls)
#             cls._instance.engine = create_engine(db_url)
#             Session = sessionmaker(bind=cls._instance.engine)
#             cls._instance.session = Session()
#         return cls._instance

#     def save_transaction(self, description, amount):
#         transaction = Transaction(description=description, amount=amount)
#         self.session.add(transaction)
#         self.session.commit()

#     def save_transactions(self, transactions):
#         for description, amount in transactions:
#             self.save_transaction(description, amount)

#     def get_transaction(self, transaction_id):
#         return self.session.query(Transaction).filter_by(id=transaction_id).first()

#     def get_transactions(self):
#         return self.session.query(Transaction).all()