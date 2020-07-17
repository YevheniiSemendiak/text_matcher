
import pymongo
import urllib.parse
import logging
import os

from typing import Mapping, Union, List


class Singleton(type):
    """
        Meta class. Ensures that class has only one instance.
    https://sourcemaking.com/design_patterns/singleton
    https://sourcemaking.com/design_patterns/singleton/python/1
    """

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class MongoDBDAO(metaclass=Singleton):
    '''
    This class plays a role of the Data Access Object (DAO) for MongoDB.
    It contains main CRUD operations (Create, Read, Update and Delete), used by BRISE to operate with a database
    '''
    def __init__(self, mongo_host: str, mongo_port: int, database_name: str, user: str, passwd: str):
        username = urllib.parse.quote_plus(user)
        password = urllib.parse.quote_plus(passwd)
        self.client = pymongo.MongoClient(
            f"mongodb://{user}:{passwd}@{mongo_host}:{mongo_port}/?authSource=admin"
            # mongo_host + ":" + str(mongo_port), username=username, password=password, authSource="admin"
        )
        self.database = self.client[database_name]
        self.logger = logging.getLogger(__name__)

    def write_one_record(self, collection_name: str, record: Mapping) -> None:
        collection = self.database[collection_name]
        x = collection.insert_one(record)
        self.logger.debug("Written to mongo. Id: " + str(x.inserted_id))

    def write_many_records(self, collection_name: str, records: List[Mapping]) -> None:
        collection = self.database[collection_name]
        x = collection.insert_many(records)
        self.logger.debug("Written many to mongo. Id: " + str(x.inserted_ids))

    def get_records(self,
                    collection_name: str,
                    filter_: Union[Mapping, None],
                    projection: Union[Mapping, List, None]) -> List[Mapping]:
        result = []
        collection = self.database[collection_name]
        for record in collection.find(filter_, projection=projection):
            result.append(dict(record))
        return result

    def get_last_record(self,
                        collection_name: str,
                        filter_: Union[Mapping, None],
                        projection: Union[Mapping, List, None]) -> Union[Mapping, None]:
        collection = self.database[collection_name]
        records = collection.find(filter_, projection=projection)
        if records.count() > 0:
            for record in records.skip(records.count() - 1):
                return dict(record)
        else:
            return None

    def update_record(self, collection_name: str, filter_: Mapping, new_val: Mapping) -> None:
        collection = self.database[collection_name]
        new_values = {"$set": new_val}
        collection.update_one(filter_, new_values)
