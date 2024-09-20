from pymongo import MongoClient
from pymongo import server_api
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

uri = os.getenv("MONGO_URI")

client = MongoClient(uri, server_api=server_api.ServerApi('1'))
db = client.mercadolivre