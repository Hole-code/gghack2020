from pymongo import MongoClient, errors
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.results import DeleteResult

from bson.objectid import ObjectId

from typing import Optional, Union, Dict


class DataBase:
    def __init__(self, db_uri: str, db_name: str) -> None:
        try:
            self._client: MongoClient = MongoClient(
                host = db_uri,
                connect = False,
                serverSelectionTimeoutMS = 2000
            )

        except errors.ConnectionFailure:
            raise Exception("Can`t connect to server!")

        self._db: DataBase = self._client.get_database(db_name)
        self._tasks: Collection = self._db.get_collection("tasks")
        self._tasklists: Collection = self._db.get_collection("tasklists")

    def add_tasklist(self, name: str, last_updated: int, created_at: int) -> ObjectId:
        return self._tasklists.insert_one({
            "name": name,
            "last_updated": last_updated,
            "created_at": created_at
        }).inserted_id

    def get_tasklist(self, tasklist_id: Optional[str]=None) -> Union[Cursor, dict]:
        if tasklist_id:
            return self._tasklists.find_one({
                "_id": ObjectId(tasklist_id)
            })

        return self._tasklists.find({})

    def edit_tasklist(self, tasklist_id: str, data: dict) -> int:
        return self._tasklists.update_one(
            {"_id": ObjectId(tasklist_id)},
            {"$set": data}
        ).modified_count

    def delete_tasklist(self, tasklist_id: Optional[str]=None) -> int:
        if tasklist_id:
            result: DeleteResult = self._tasklists.delete_one({
                "_id": ObjectId(tasklist_id)
            })

        else:
            result: DeleteResult = self._tasklists.delete_many({})

        return result.deleted_count

    def add_task(self, name: str, last_updated: str, created_at: str, description: str, tasklist_id: str) -> ObjectId:
        return self._tasks.insert_one({
            "name": name,
            "last_updated": last_updated,
            "created_at": created_at,
            "description": description,
            "tasklist_id": ObjectId(tasklist_id)
        }).inserted_id

    def get_task(self, task_id: Optional[str]=None, tasklist_id: Optional[str]=None) -> Union[Cursor, dict]:
        if task_id:
            return self._tasks.find_one({
                "_id": ObjectId(task_id)
            })

        elif tasklist_id:
            return self._tasks.find({
                "tasklist_id": ObjectId(tasklist_id)
            })

        return self._tasks.find({})

    def edit_task(self, task_id: str, data: dict) -> int:
        return self._tasks.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": data}
        ).modified_count

    def delete_task(self, task_id: Optional[str]=None) -> int:
        if task_id:
            result: DeleteResult = self._tasks.delete_one({
                "_id": ObjectId(task_id)
            })

        else:
            result: DeleteResult = self._tasks.delete_many({})

        return result.deleted_count

    def close(self) -> None:
        self._client.close()
