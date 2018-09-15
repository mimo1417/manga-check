"""storage for the manga

format:
    id,chapter,is_read
"""
import os
import json
import traceback

import pymongo

from manga_check.config import MANGA_MONGO_DB, MONGO_COLLECTION, MANGAS

# init
_dir = os.path.dirname(os.path.abspath(__file__))


class Storage(object):

    def __init__(self):
        try:
            self.storage = MongoStorage()
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            print("cannot connect main storage, using local")
            self.storage = LocalStorage()

    def get(self):
        return self.storage.get()

    def update(self, data):
        self.storage.update(data)

    def clean(self):
        self.storage.clean()


class MongoStorage(object):

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
            bool: updated or not
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


class LocalStorage(object):
    """Just in case the Mongo is not available
    """

    FILENAME = os.path.join(_dir, 'manga_check.json')

    def __init__(self):
        if not os.path.exists(self.FILENAME):
            with open(self.FILENAME, 'w') as f:
                self.data = [{
                    'id': manga['id'],
                    'chapter': 0,
                    'is_read': False,
                }
                    for _, manga in MANGAS.items()]
                json.dump(self.data, fp=f)
        else:
            with open(self.FILENAME, 'r') as f:
                self.data = json.load(fp=f)

    def get(self):
        return self.data

    def update(self, data):
        self.data = [row for _, row in data.items()]
        with open(self.FILENAME, 'w') as f:
            json.dump(self.data, fp=f)

    def clean(self):
        """clean all data"""
        os.remove(self.FILENAME)
