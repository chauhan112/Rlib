
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
db = SqliteDatabase(dbPath, pragmas={'foreign_keys': 1})


class JSONField(TextField):
    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)

class BaseModel(Model):
    class Meta:
        database = db

def currentISO():
    return datetime.now().isoformat()

class Job(BaseModel):
    created_on = DateTimeField(default=currentISO)
    modified_on = DateTimeField(default=currentISO)
    title = CharField(null=True)
    description = TextField(null=True)
    summary = TextField(null=True)
    link = CharField(null=True)
    more_info = JSONField(null=True)

class JobCV(BaseModel):
    created_on = DateTimeField(default=currentISO)
    modified_on = DateTimeField(default=currentISO)
    content = TextField(null=True) # cv content only
    all_content = TextField(null=True) # cv content + think tag
    job = ForeignKeyField(Job, backref='cvs')
class MotivationCV(BaseModel):
    created_on = DateTimeField(default=currentISO)
    modified_on = DateTimeField(default=currentISO)
    content = TextField(null=True)
    all_content = TextField(null=True)
    job = ForeignKeyField(Job, backref='cvs', null=True)
def create_tables_for_job_cv(deletePrevious = False):
    db.connect()
    if deletePrevious:
        db.drop_tables([Job, JobCV, MotivationCV], safe=True)
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
def get_table(name:str):
    names = {
        'Job':Job,
        'JobCV':JobCV,
        'MotivationCV':MotivationCV
    }
    return names[name]

@connectionWrapper
def addData(tableName:str, data):
    table = get_table(tableName)
    table.create(**data)
@connectionWrapper
def deleteDataWhere(tableName:str, data):
    table = get_table(tableName)
    table.delete().where(**data).execute()
@connectionWrapper
def deleteDataWithId(tableName:str, id:int):
    table = get_table(tableName)
    table.delete().where(table.id == id).execute()
@connectionWrapper
def updateData(tableName:str, id:int, data):
    table = get_table(tableName)
    table.update(**data).where(table.id == id).execute()
@connectionWrapper
def readAsDic(tableName:str, id:int):
    table = get_table(tableName)
    data = table.select().where(table.id == id).get()
    return data.__data__
@connectionWrapper
def readAllWithPagination(tableName:str, page:int, perPage:int):
    table = get_table(tableName)
    data = table.select().paginate(page, perPage)
    return selectResToList(data)
@connectionWrapper
def readWhere(tableName:str, data):
    table = get_table(tableName)
    conditions = []
    for k, v in data.items():
        conditions.append(getattr(table, k) == v)
    data = table.select().where(*conditions)
    return selectResToList(data)
@connectionWrapper
def readAll(tableName:str):
    table = get_table(tableName)
    data = table.select()
    return selectResToList(data)
