from ndb.ndb import NDBClient
from ndb.ndb import NDB

client = NDBClient(NDB("http://localhost:3000"), "id", "pw", "database", "coll")

print(client.get_whole_document())