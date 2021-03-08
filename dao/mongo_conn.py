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


if __name__ == '__main__':
    print(111)
    # obj = MongoConn(host=current_app.config['mongo_params']['host'],
    #                 user=current_app.config['mongo_params']['user'],
    #                 password=params['password'], database=params['database'], collection=params['collection'])
    # rest = obj.find(projection={'productClass': 1, '_id': 0}).limit(100)
    # for productClass in rest:
    #     print(productClass)


