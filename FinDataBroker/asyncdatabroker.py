from typing import Any, Dict, List, Tuple, Union

from pymongo.errors import BulkWriteErro


class DataBrokerMongoDb:
    """
    DataBroker that interacts with mongodb.
    """

    def __init__(self, client):
        self.client = client

    async def save(
        self,
        data: Union[List[Dict], Dict],
        db: str,
        col: str,
        indexTupleList: List[Tuple[str, Any]],
        unique=True,
    ):
        """
        Public method to save the data to a collection.

        User should take care that data is given
        in the correct format (list of dicts, bjson)

        :param data: data to save
        :param db: database name
        :param col: collection name
        :param indexTupleList:tuples define the index
        :param unique: index keys unique ? (default: True)
        """
        colm = self.client[db][col]
        await colm.create_index(indexTupleList, unique=unique)

        if not isinstance(data, list):
            datal: List = [data]
        else:
            datal = data

        try:
            await colm.insert_many(datal, ordered=False)
        except BulkWriteError:
            pass

    async def load(self, db: str, col: str, searchdict: Dict):
        """
        Publid method to load data from the database.

        :param db: database name
        :param col: collection name
        :param searchdict: mongo valid search dict
        :return: requested data as list of dicts
        """
        colm = self.client[db][col]
        cursor = colm.find(searchdict, {"_id": False})

        out = []
        async for doc in cursor:
            out.append(doc)

        return out
