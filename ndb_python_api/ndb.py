import json
import requests
from ndb_python_api.roles import Roles

class NDB:
    def __init__(self, uri):
        self.uri = uri


class NDBClient:
    def __init__(self, ndb: NDB, id: str, pw: str, db: str, coll: str):
        self.ndb = ndb
        self.id = id
        self.pw = pw
        self.db = db
        self.coll = coll
        self.db_url = f"{ndb.uri}/ndb/collection?id={id}&pw={pw}&dbName={db}&collectionName={coll}"
        self.manage_url = f"{ndb.uri}/ndb/create?id={id}&pw={pw}"

    def create_user(self, id, pw, roles: Roles):
        creation_string = f"{id}:{pw}:{roles.role}"
        res = requests.get(f"{self.manage_url}&user={creation_string}")
        return res.json() if res.ok else None

    def create_database(self, db_name, collection_name):
        res = requests.get(f"{self.manage_url}&database={db_name}&collection={collection_name}")
        return res.json() if res.ok else None

    def get_whole_document(self):
        res = requests.get(self.db_url)
        return res.json() if res.ok else None

    def get_document(self, key):
        res = requests.get(f"{self.db_url}&findBy={key}")
        return res.json() if res.ok else None

    def edit_document(self, document_key, json_object):
        res = requests.get(f"{self.db_url}&findBy={document_key}&edit={json.dumps(json_object)}")
        return res.json() if res.ok else None

    def add_document_field_array_or_list(self, document_key, field, field_array):
        res = requests.get(f"{self.db_url}&findBy={document_key}&addField={field}&fieldArray={json.dumps(field_array)}")
        return res.json() if res.ok else None

    def add_document_field_value(self, document_key, field, field_value, is_strict=False):
        res = requests.get(f"{self.db_url}&findBy={document_key}&addField={field}&fieldValue={json.dumps(field_value)}&isStrict={str(is_strict).lower()}")
        return res.json() if res.ok else None

    def delete_document_field_value(self, document_key, field):
        res = requests.get(f"{self.db_url}&findBy={document_key}&deleteField={field}")
        return res.json() if res.ok else None

    def add_or_replace_document(self, key, value):
        res = requests.get(f"{self.db_url}&addKey={key}&keyValue={json.dumps(value)}")
        return res.json() if res.ok else None

    def delete_document(self, key):
        res = requests.get(f"{self.db_url}&deleteKey={key}")
        return res.json() if res.ok else None

    def find_document(self, key):
        json_data = self.get_whole_document()
        if json_data and key in json_data:
            return json_data[key]
        return None

    def get_field_value(self, document, field):
        return document.get(field)

    def edit_or_insert_field(self, document_key, field, value):
        self.delete_document_field_value(document_key, field)
        if isinstance(value, dict):
            return self.add_document_field_array_or_list(document_key, field, value)
        else:
            return self.add_document_field_value(document_key, field, value)

    def edit_or_insert_field_as_strict(self, document_key, field, value):
        self.delete_document_field_value(document_key, field)
        if isinstance(value, dict):
            return self.add_document_field_array_or_list(document_key, field, value)
        else:
            return self.add_document_field_value(document_key, field, value, is_strict=True)

    def edit_map_to_json_object(self, map_data):
        json_map = {}
        for key, value in map_data.items():
            if isinstance(key, str):
                if isinstance(value, dict):
                    json_element = self.edit_map_to_json_object(value)
                elif isinstance(value, list):
                    json_element = self.edit_list_to_array(value)
                elif isinstance(value, (int, bool, str)):
                    json_element = value
                else:
                    json_element = None
                if json_element is not None:
                    json_map[key] = json_element
        return json_map

    def edit_list_to_array(self, list_data):
        result = []
        for value in list_data:
            if isinstance(value, str):
                try:
                    parsed_list = [int(x.strip()) for x in value.split(',')]
                    result.extend(parsed_list)
                except ValueError:
                    result.append(value)
            elif isinstance(value, dict):
                result.append(self.edit_map_to_json_object(value))
            elif isinstance(value, list):
                result.extend(self.edit_list_to_array(value))
            elif isinstance(value, (int, bool)):
                result.append(value)
            else:
                result.append(None)
        return result
