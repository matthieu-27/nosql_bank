from pymongo import MongoClient
from config import MONGODB_URI, DB_NAME

_client = None


def get_db():
    global _client
    if _client is None:
        _client = MongoClient(MONGODB_URI)
    return _client[DB_NAME]


def next_id(collection_name: str, prefix: str) -> str:
    db = get_db()
    docs = list(db[collection_name].find({}, {"_id": 1}))
    ids = [
        doc["_id"]
        for doc in docs
        if isinstance(doc["_id"], str) and doc["_id"].startswith(prefix)
    ]
    if not ids:
        return f"{prefix}001"
    nums = [int(id_[len(prefix):]) for id_ in ids]
    return f"{prefix}{max(nums) + 1:03d}"
