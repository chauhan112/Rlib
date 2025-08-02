from peewee import TextField, CharField, DateTimeField
from datetime import datetime
from ...Aug.cvMotivationMaker.db import BaseModel, db

class UrlsCollection(BaseModel):
    created_on = DateTimeField(default=datetime.now)
    modified_on = DateTimeField(default=datetime.now)
    name = CharField(null=True)
    description = TextField(null=True)

class UrlLink(BaseModel):
    created_on = DateTimeField(default=datetime.now)
    modified_on = DateTimeField(default=datetime.now)
    url = CharField(null=True)
    title = CharField(null=True)

def create_tables_for_url_links():
    with db:
        db.create_tables([UrlsCollection, UrlLink], safe=True)