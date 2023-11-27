import pymongo

class MongoQueries:
    def __init__(self):
        self.host = "localhost"
        self.port = 27017
        self.serviceName = 'bancoDadosMDB'

        #with open("conexion/passphrase/authentication.mongo", "r") as f:
        #    self.user, self.password = f.read().split(',')

    def __del__(self):
        if hasattr(self, "mongoClient"):
            self.close()

    def connect(self):
        self.mongoClient = pymongo.MongoClient(f"mongodb://localhost:27017/")
        self.db = self.mongoClient["bancoDadosMDB"]

    def close(self):
        self.mongoClient.close()