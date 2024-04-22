from peewee import SqliteDatabase, Model, CharField, ForeignKeyField, TextField, DateTimeField, BooleanField, DatabaseProxy,SQL
import datetime

db_proxy = DatabaseProxy()
class BaseModel(Model):
    class Meta:
        database = db_proxy
class LocalStorage(BaseModel):
    app_name = CharField()
    key = TextField()
    value = TextField()
    class Meta:
        constraints = [SQL('UNIQUE (app_name, key)')]
class SyntaxLanguage(BaseModel):
    name = CharField(unique=True)
class SyntaxContent(BaseModel):
    language = ForeignKeyField(SyntaxLanguage, backref='contents')
    content = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)
    updated_date = DateTimeField(default=datetime.datetime.now)

from basic import NameSpace
ns = NameSpace()
ns.SyntaxLanguage = SyntaxLanguage
ns.SyntaxContent = SyntaxContent
ns.LocalStorage = LocalStorage
