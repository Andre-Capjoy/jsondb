import json
import hashlib

class jsonDB:
    def __init__(self, file_name: str):
        self.file_name = file_name
        
    def collection(self, collection_name):
        return jsonCollection(self, collection_name)
    
    def getDB(self):
        try:
            with open(self.file_name, encoding='utf8') as f:
                data = json.load(f)
        except:
            data = {}
        
        return data
    
    def writeDB(self, data):
        with open(self.file_name, 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

class jsonCollection(jsonDB):
    
    def __init__(self, masterClass, collection_name: str):
        # inherit all vars from jsonDB class
        self.__dict__ = masterClass.__dict__
                
        self.collection_name = collection_name
        
    def insert_one(self, python_dict: dict):
        coll = self.getColl()
        
        python_dict["_id"] = hashlib.md5(str(python_dict).encode()).hexdigest()
        
        try:
            if not any(entry["_id"] == python_dict["_id"] for entry in coll):
                coll.append(python_dict)
                self.writeColl(coll)
        except:
            return -1
        
        return python_dict["_id"]
    
    def insert_many(self, dict_list : list):
        id_list : list = []
        for item in dict_list:
            id_list.append(self.insert_one(item))
            
        return id_list
    
    def getColl(self):
        dict = self.getDB()
        try: 
            coll = dict[self.collection_name]["items"]
        except KeyError:
            coll = []
        return coll

    def writeColl(self, coll):
        dict = self.getDB()
        try:
            dict[self.collection_name]["items"] = coll
        except KeyError:
            dict = { self.collection_name : {} }
            dict[self.collection_name]["items"] = coll
        self.writeDB(dict)
