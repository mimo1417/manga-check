"""storage for the manga

format:
    id,chapter,is_read
"""
import traceback
import pymongo
from manga_check.config import MANGA_MONGO_DB, MONGO_COLLECTION


class Storage(object):

    def __init__(self):
        self.client = pymongo.MongoClient(MANGA_MONGO_DB)
        self.collection = self.client.get_database().get_collection(MONGO_COLLECTION)

    def get(self):
        try:
            data = self.collection.find({}, {'_id': 0})
            return list(data)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            return []

    def update(self, data):
        """store data to storage
        
        Args:
            data (list): store data
        
        Returns:
            boolean: updated or not
        """
        operations = [
            pymongo.UpdateOne({'id': row['id']}, {
                '$set': {
                    'chapter': row['chapter'], 
                    'is_read': row['is_read']
                }
            }, upsert=True)
            for id, row in data.items()
        ]
        try:
            self.collection.bulk_write(operations)
            return True
        except pymongo.errors.BulkWriteError as e:
            print(e)
            print(traceback.format_exc())
            return False

    def clean(self):
        """clean all data"""
        self.collection.delete_many({})
