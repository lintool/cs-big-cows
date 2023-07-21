import pymongo
from mongodb.datamodel import AuthorPublications

# credential
password = "asdfghjkl"

class MongoDBAPI:
    def __init__(self, database_name, collection_name):
        self.client = pymongo.MongoClient(
            f"mongodb+srv://researcherGPT:{password}@researchergpt.oquqsqd.mongodb.net/?retryWrites=true&w=majority",
            serverSelectionTimeoutMS=60000
        )
        self.database_name = database_name
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def insert_data(self, datamodel, data):
        # Validate data against the data model schema
        if not all(datamodel.validate_data(d) for d in data):
            raise ValueError("Invalid data format. Data does not match the data model schema.")

        # Insert the data into the collection
        bp()
        insert_result = self.collection.insert_many(data)
        return insert_result.inserted_ids
    
class PublicationDB(MongoDBAPI):
    def __init__(self, award_name):
        super().__init__(database_name="acm_db", collection_name=award_name)
    
    def insert_data(self, data):
        return super().insert_data(AuthorPublications, data)