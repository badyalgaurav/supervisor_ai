from pymongo import MongoClient


def get_mongo_client():
    server_address = "127.0.0.1:27017"
    client = MongoClient(f"mongodb://{server_address}")
    return client
