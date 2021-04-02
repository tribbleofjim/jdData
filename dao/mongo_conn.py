import pymongo
from bson import ObjectId


class MongoConn(object):

    def __init__(self
                 , host='127.0.0.1'
                 , port=27017
                 , user=None
                 , password=None
                 , database=None
                 , collection=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.collection = collection

        url = 'mongodb://{}:{}@{}:{}/?authSource={}' \
            .format(user, password, host, port, database)
        self.conn = pymongo.MongoClient(url)
        self.db = self.conn[database]

    def add_one(self
                , data
                , collection=None):
        coll = collection if self.collection is None else self.collection
        res = self.db[coll].insert_one(data)
        return res

    def add_many(self, data, collection=None):
        coll = collection if self.collection is None else self.collection
        res = self.db[coll].insert_many(data)
        return res

    def get_count(self, collection=None):
        coll = collection if self.collection is None else self.collection
        self.db[coll].count()

    def find_one(self, collection=None, query=None, projection=None):
        coll = collection if self.collection is None else self.collection
        return self.db[coll].find_one(query, projection)

    def find(self, collection=None, query=None, projection=None):
        coll = collection if self.collection is None else self.collection
        return self.db[coll].find(query, projection)

    def get_from_oid(self, oid, collection=None):
        coll = collection if self.collection is None else self.collection
        return self.db[coll].find_one({'_id': ObjectId(oid)})

    def aggregate(self, collection=None):
        coll = collection if self.collection is None else self.collection
        return self.db[coll].aggregate()

    def delete_one(self, cond=None, collection=None):
        coll = collection if self.collection is None else self.collection
        if cond:
            return self.db[coll].delete_one(filter=cond, collation=coll)
        else:
            return self.db[coll].delete_one(collation=coll)

    def delete_many(self, cond=None, collection=None):
        coll = collection if self.collection is None else self.collection
        if cond:
            return self.db[coll].delete_many(filter=cond, collation=coll)
        else:
            return self.db[coll].delete_many(collation=coll)

    def update_one(self, cond=None, collection=None):
        coll = collection if self.collection is None else self.collection
        if cond:
            return self.db[coll].update_one(filter=cond, collation=coll)
        else:
            return self.db[coll].update_one(collation=coll)

    def update_many(self, cond=None, collection=None):
        coll = collection if self.collection is None else self.collection
        if cond:
            return self.db[coll].update_many(filter=cond, collation=coll)
        else:
            return self.db[coll].update_many(collation=coll)

    def drop(self, collection=None):
        coll = collection if self.collection is None else self.collection
        self.db[coll].drop()

    def drop_index(self, index, collection=None):
        coll = collection if self.collection is None else self.collection
        self.db[coll].drop_index(index_or_name=index)

    def drop_indexes(self, index, collection=None):
        coll = collection if self.collection is None else self.collection
        self.db[coll].drop_indexes()


if __name__ == '__main__':
    print(111)
    # obj = MongoConn(host=current_app.config['mongo_params']['host'],
    #                 user=current_app.config['mongo_params']['user'],
    #                 password=params['password'], database=params['database'], collection=params['collection'])
    # rest = obj.find(projection={'productClass': 1, '_id': 0}).limit(100)
    # for productClass in rest:
    #     print(productClass)


