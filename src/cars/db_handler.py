from pymongo.mongo_client import MongoClient
from enum import Enum

uri = 'mongodb+srv://root:12345@cluster0.zrfqev1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'


class CarAttribute(Enum):
    MAKE = 'make'
    MODEL = 'model'
    RATES_SUM = 'rates_sum'
    RATES_NUM = 'rates_num'


class DBHandler:

    def __init__(self, db_name: str, collection_name: str) -> None:
        self._client = None
        self._db = None
        self._collection_name = collection_name

        self._connect()
        self._db = self._client[db_name]

    def _connect(self) -> None:
        self._client = MongoClient(uri)

        try:
            self._client.admin.command('ping')
        except Exception as e:
            self._client = None
            raise e
        
    def reset(self) -> None:
        self._db[self._collection_name].delete_many({})

    def get_car(self, make: str, model: str) -> dict[str, str, int, int] | None:
        result = self._db[self._collection_name].find_one({
            '_id': {CarAttribute.MAKE.value: make, CarAttribute.MODEL.value: model},
        })

        return result

    def car_exists(self, make: str, model: str) -> bool:
        return self.get_car(make, model) != None

    def insert_car(self, make: str, model: str) -> None:
        if self.car_exists(make, model):
            raise Exception('Given car already exists in the database')

        result = self._db[self._collection_name].insert_one({
            '_id': {CarAttribute.MAKE.value: make, CarAttribute.MODEL.value: model},
            CarAttribute.RATES_SUM.value: 0,
            CarAttribute.RATES_NUM.value: 0
        })
    
        if not result.acknowledged:
            raise Exception('Car insertion has failed')

    def update_rate(self, make: str, model: str, rate: int) -> None:
        if not self.car_exists(make, model):
            raise Exception('Given car does not exist in the database')

        result = self._db[self._collection_name].update_one(
            {'_id': {CarAttribute.MAKE.value: make, CarAttribute.MODEL.value: model}},
            {'$inc': {CarAttribute.RATES_SUM.value: rate, CarAttribute.RATES_NUM.value: 1}}
        )

        if not result.acknowledged:
            raise Exception('Adding a rate has failed')
        
    def get_all_cars(self) -> list[dict[str, str, float | None]]:
        cursor = self._db[self._collection_name].aggregate([
            { '$project': {
                '_id': 0,
                CarAttribute.MAKE.value: '$_id.{}'.format(CarAttribute.MAKE.value),
                CarAttribute.MODEL.value: '$_id.{}'.format(CarAttribute.MODEL.value),
                'rate_avg': {'$cond': [{ '$eq': ['${}'.format(CarAttribute.RATES_NUM.value), 0]}, None, {'$divide': ['${}'.format(CarAttribute.RATES_SUM.value), '${}'.format(CarAttribute.RATES_NUM.value)]}]},
            }}
        ])
        
        return list(cursor)
    
    def get_popular_cars(self, top_n: int) -> list[dict[str, str]]:
        cursor = self._db[self._collection_name].aggregate([
            {'$project': {
                '_id': 0,
                CarAttribute.MAKE.value: '$_id.{}'.format(CarAttribute.MAKE.value),
                CarAttribute.MODEL.value: '$_id.{}'.format(CarAttribute.MODEL.value)
            }},

            {'$sort': {CarAttribute.RATES_NUM.value: -1}},
            {'$limit': top_n}
        ])

        return list(cursor)
