from pymongo import MongoClient
from datetime import datetime

class PrizeRepository:
    def __init__(self, db_name: str, db_url: str):
        print(f'Initiating PrizeRepository, variables: \ndb_url: {db_url}, db_name: {db_name}')
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db['premios']
        self.db_name = db_name
        self.db_url = db_url

    def get_all_prizes(self) -> list:
        print('In PrizeRepository, method: get_all_prizes')
        prizes = []
        for data in self.collection.find():
            data['id'] = str(data.get('_id'))
            data.pop('_id', None)
            prizes.append(data)
        return prizes

    def update_prizes(self, prizes_list: list) -> bool:
        print(f'In PrizeRepository, method: update_prizes, variables: \nprizes_list: {prizes_list}')
        try:
            # clear existing prizes and insert new ones
            self.collection.delete_many({})
            if prizes_list:
                # Ensure each item is a dict
                to_insert = []
                for p in prizes_list:
                    if isinstance(p, dict):
                        to_insert.append(p.copy())
                    else:
                        # try to coerce simple tuples/lists
                        to_insert.append({'premio': str(p)})
                self.collection.insert_many(to_insert)
            return True
        except Exception as e:
            print(f'Error updating prizes in DB: {e}')
            return False
