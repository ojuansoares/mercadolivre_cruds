from pymongo import MongoClient
from pymongo import server_api
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

uri = os.getenv("MONGO_URI")

client = MongoClient(uri, server_api=server_api.ServerApi('1'))
db = client.mercadolivre

def check_mongodb_connection():
    try:
        # The ping command is cheap and does not require auth.
        client.admin.command('ping')
        print("Conectado ao MongoDB!")
    except Exception as e:
        print(f"An error occurred: {e}")