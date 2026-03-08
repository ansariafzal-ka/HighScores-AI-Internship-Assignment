import sys
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from src.utils.exception import CustomException

class MongoDBConnection:
    """
    This class will connect to the remote Mongodb Atlas where the data is stored.
    """
    client = None
    database = None
    def __init__(self) -> None:
        try:
            load_dotenv()
            if MongoDBConnection.client is None:
                self.initialise_mongodb()
            self.database = MongoDBConnection.database
        except Exception as e:
            raise CustomException(e, sys)
        
    def initialise_mongodb(self) -> None:
        try:
            MONGODB_URI = os.getenv('MONGODB_URI')
            MONGODB_DATABASE = os.getenv('MONGODB_DATABASE')
            MongoDBConnection.client = MongoClient(MONGODB_URI)
            MongoDBConnection.database = MongoDBConnection.client[MONGODB_DATABASE]
            print('Connected to MongoDB.')
        except Exception as e:
            raise CustomException(e, sys)
        
connection = MongoDBConnection()
db = connection.database