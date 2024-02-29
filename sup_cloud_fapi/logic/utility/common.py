from pymongo import MongoClient


def get_mongo_client():
    client = MongoClient(f"mongodb://interx:interx%40504@server.interxlab.io:15115/admin")
    return client
