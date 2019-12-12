from .Template import DataBroker
from pprint import pprint
from typing import List, Tuple
from tqdm import tqdm
from termcolor import colored

class DataBrokerMongoDb(DataBroker):
    """
    DataBroker that interacts with mongodb.
    """

    def __init__(self, client):
        super(DataBrokerMongoDb, self).__init__()
        self.client = client

    def get_stats(self, db):
        """
        Prints the collections in the given database and
        the dbstats.

        :param db: database name
        :type db: str
                database name for which one
                would like to get the stats
        """
        # with self.client:
        dbm = self.client[db]
        print(dbm.collection_names())
        status = dbm.command('dbstats')

        pprint(status)

    def get_number_of_documents(self, db: str, col: str) -> int:
        """
        Get the total number of documents
        stored in the collection col
        from the database db
        :param db: database name
        :type db: str
        :param col: collection name
        :type col: str

        :return: number of documents stored in col
        """
        # with self.client:
        colm = self.client[db][col]
        n = colm.count_documents({})

        return n

    def _create_index(self, db: str, col: str, indexTupleList: List[Tuple], unique=True):
        """
        Private method to create index if
        it does not already exists.

        :param db: database name
        :type db: str
        :param col: collection name
        :type col: str
        :param indexTupleList: list of tuples to create index
        :type indexTupleList: list of tuples
              the tuples are (field, ASCENDING/DESCENDING)
        :param unique:
        :type unique: bool
                Default : True (allows double check to prevent duplicates)

        """
        # with self.client:
        colm = self.client[db][col]
        colm.create_index(indexTupleList, unique=unique)

    def save(self, data, db: str, col: str, indexTupleList: List[Tuple], unique=True):
        """
        Public method to save the data to
        a collection.

        User should take care that data is given
        in the correct format (list of dicts, bjson)

        :param data: data to save
        :type data: list of dicts (bjson)
        :param db: database name
        :type db: str
        :param col: collection name
            str
        :param indexTupleList:
            list of tuples
                tuples define the index
        :param unique:
            bool
                default true
        """
        self._create_index(db, col, indexTupleList, unique=unique)
        # with self.client as client:
        colm = self.client[db][col]
        # ref : https://docs.mongodb.com/php-library/master/reference/method/MongoDBCollection-insertMany/
        # ordered False will continue writing if one fails
        temp = None
        if not isinstance(data, list):
            data = [data]

        for row in tqdm(data):
            # db.collection.count_documents({ 'UserIDS': newID }, limit = 1) != 0
            try:
                if colm.count_documents({k[0]: row[k[0]] for k in indexTupleList}, limit=1) == 0:
                    colm.insert_one(row)
                else:
                    if temp == row[indexTupleList[0][0]]:
                        continue
                    else:
                        temp = row[indexTupleList[0][0]]

                        _list = [str(row[k[0]]) for k in indexTupleList]
                        tup = ','.join(_list)
                        print(colored(f"{tup} already exists", 'red'))
            except:
                print([k[0] for k in indexTupleList])
                print(row)
                break
            # colm.insert_many(data, ordered=False)

    def load(self, db, col, searchdict):
        """
        Publid method to load data from the database.

        :param db: database name
            str
        :param col: collection name
            str
        :param searchdict: mongo valid search dict
            dict

        :return: requested data as list of dicts
        """
        # with self.client as client:
        colm = self.client[db][col]
        return list(colm.find(searchdict, {'_id': False}))
