from pprint import pprint
from typing import Any, Dict, List, Tuple, Union

from pymongo.errors import BulkWriteError
from termcolor import colored
from tqdm import tqdm

from .Template import DataBroker


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
        dbm = self.client[db]

        print(sorted(dbm.collection_names()))
        status = dbm.command("dbstats")

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
        colm = self.client[db][col]
        n = colm.count_documents({})

        return n

    def save(
        self,
        data: Union[List[Dict], Dict],
        db: str,
        col: str,
        indexTupleList: List[Tuple[str, Any]],
        unique: bool = True,
    ):
        """
        Public method to save the data to
        a collection.

        User should take care that data is given
        in the correct format (list of dicts, bjson)

        Arguments:
        ----------
        data: Union[List[Dict], Dict],
            data to save
        db: str
            database name
        col: str
            collection name
        indexTupleList: List[Tuple[str, Any]]
            tuples define the index
        unique: Bool
            index keys unique ? (default: True)
        """
        colm = self.client[db][col]
        colm.create_index(indexTupleList, unique=unique)

        if not isinstance(data, list):
            datal: List = [data]
        else:
            datal = data

        try:
            colm.insert_many(datal, ordered=False)
        except BulkWriteError:
            pass

    def load(self, db: str, col: str, searchdict: Dict, selectiondict={}):
        """
        Publid method to load data from the database.

        :param db: database name
        :type db: str
        :param col: collection name
            str
        :param searchdict: mongo valid search dict
            dict

        :return: requested data as list of dicts
        """
        colm = self.client[db][col]
        cursor = colm.find(searchdict, {**{"_id": False}, **selectiondict})

        out = []
        for doc in cursor:
            out.append(doc)

        return out

    def update(self, db: str, col: str, myquery, newvalues):
        """
        Public method to update records in a
        collection.

        Arguments:
        ----------
        db          : str
            database to update
        col         : str
            collection to update
        myquery     : dict
            query to select records to update
        newvalues   : mongodb set dict
            mongodb set field dict eg. { "$set": { "name": "Minnie" } }

        """
        colm = self.client[db][col]
        x = colm.update_many(myquery, newvalues)

        print(x.modified_count, "documents updated.")
