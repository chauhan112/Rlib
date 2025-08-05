
from useful.LibsDB import LibsDB
import os
from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    DateTimeField,ForeignKeyField,
    TextField
)
from datetime import datetime
import os
import json


dbPath = os.path.join(LibsDB.cloudPath(), 'Global', 'code', 'libs', 'resource', 'dbs', 'timeline', '2025', 'general.sqlite')
if not os.path.exists(dbPath):
    os.makedirs(os.path.dirname(dbPath), exist_ok=True)
db = SqliteDatabase(dbPath)


class JSONField(TextField):
    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)

class BaseModel(Model):
    class Meta:
        database = db

class Job(BaseModel):
    created_on = DateTimeField(default=datetime.now)
    modified_on = DateTimeField(default=datetime.now)
    description = CharField(null=True)
    summary = CharField(null=True)
    link = CharField(null=True)
    more_info = JSONField(null=True)

class JobCV(BaseModel):
    created_on = DateTimeField(default=datetime.now)
    modified_on = DateTimeField(default=datetime.now)
    content = CharField(null=True)
    all_content = CharField(null=True)
    job = ForeignKeyField(Job, backref='cvs', null=True)
class MotivationCV(BaseModel):
    created_on = DateTimeField(default=datetime.now)
    modified_on = DateTimeField(default=datetime.now)
    content = CharField(null=True)
    all_content = CharField(null=True)
    job = ForeignKeyField(Job, backref='cvs', null=True)

def create_tables_for_job_cv():
    db.connect()
    db.create_tables([Job, JobCV, MotivationCV], safe=True)
    db.close()

def connectionWrapper(func):
    def wrapper(*args, **kwargs):
        with db:
            result = func(*args, **kwargs)
        return result
    return wrapper
def selectResToList(res):
    return [j.__data__ for j in res]

@connectionWrapper
def addData(tableName:str, data):
    table = eval(tableName)
    table.create(**data)
@connectionWrapper
def deleteDataWhere(tableName:str, data):
    table = eval(tableName)
    table.delete().where(**data).execute()
@connectionWrapper
def deleteDataWithId(tableName:str, id:int):
    table = eval(tableName)
    table.delete().where(table.id == id).execute()
@connectionWrapper
def updateData(tableName:str, id:int, data):
    table = eval(tableName)
    table.update(**data).where(table.id == id).execute()
@connectionWrapper
def readAsDic(tableName:str, id:int):
    table = eval(tableName)
    data = table.select().where(table.id == id).get()
    return data.__data__
@connectionWrapper
def readAllWithPagination(tableName:str, page:int, perPage:int):
    table = eval(tableName)
    data = table.select().paginate(page, perPage)
    return selectResToList(data)
@connectionWrapper
def readWhere(tableName:str, data):
    table = eval(tableName)
    data = table.select().where(**data)
    return selectResToList(data)
@connectionWrapper
def readAll(tableName:str):
    table = eval(tableName)
    data = table.select()
    return selectResToList(data)
