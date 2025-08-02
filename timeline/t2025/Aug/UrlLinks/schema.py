from typing import List, Optional
from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter

# schema.py
import strawberry
from typing import List, Optional
from .models import UrlsCollection, UrlLink, db
from datetime import datetime
from peewee import IntegrityError

# --- GraphQL Types ---

@strawberry.type
class UrlLinkType:
    id: int
    url: str
    title: str
    created_on: datetime
    modified_on: datetime

@strawberry.type
class UrlsCollectionType:
    id: int
    name: str
    description: Optional[str]
    created_on: datetime
    modified_on: datetime

    @strawberry.field
    def links(self) -> List[UrlLinkType]:
        return [UrlLinkType(id=link.id, url=link.url, title=link.title, created_on=link.created_on, modified_on=link.modified_on) for link in UrlLink.select().where(UrlLink.collection_id == self.id)]

# --- Input Types for Mutations ---

@strawberry.input
class AddUrlsCollectionInput:
    name: str
    description: Optional[str] = None

@strawberry.input
class AddUrlLinkInput:
    url: str
    title: str
    collection_id: Optional[int] = None

@strawberry.input
class UpdateUrlsCollectionInput:
    id: int
    name: Optional[str] = None
    description: Optional[str] = None

@strawberry.input
class UpdateUrlLinkInput:
    id: int
    url: Optional[str] = None
    title: Optional[str] = None
    collection_id: Optional[int] = None

# --- Queries ---

@strawberry.type
class Query:
    @strawberry.field
    def all_collections(self) -> List[UrlsCollectionType]:
        with db.connection_context():
            return [UrlsCollectionType(id=col.id, name=col.name, description=col.description, created_on=col.created_on, modified_on=col.modified_on) for col in UrlsCollection.select()]

    @strawberry.field
    def collection_by_id(self, id: int) -> Optional[UrlsCollectionType]:
        with db.connection_context():
            collection = UrlsCollection.get_or_none(UrlsCollection.id == id)
            if collection:
                return UrlsCollectionType(id=collection.id, name=collection.name, description=collection.description, created_on=collection.created_on, modified_on=collection.modified_on)
            return None

    @strawberry.field
    def all_links(self) -> List[UrlLinkType]:
        with db.connection_context():
            return [UrlLinkType(id=link.id, url=link.url, title=link.title, created_on=link.created_on, modified_on=link.modified_on) for link in UrlLink.select()]

    @strawberry.field
    def link_by_id(self, id: int) -> Optional[UrlLinkType]:
        with db.connection_context():
            link = UrlLink.get_or_none(UrlLink.id == id)
            if link:
                return UrlLinkType(id=link.id, url=link.url, title=link.title, created_on=link.created_on, modified_on=link.modified_on)
            return None

# --- Mutations ---

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_collection(self, collection_input: AddUrlsCollectionInput) -> UrlsCollectionType:
        with db.connection_context():
            try:
                new_collection = UrlsCollection.create(
                    name=collection_input.name,
                    description=collection_input.description
                )
                return UrlsCollectionType(id=new_collection.id, name=new_collection.name, description=new_collection.description, created_on=new_collection.created_on, modified_on=new_collection.modified_on)
            except IntegrityError:
                raise Exception("A collection with this name already exists.")

    @strawberry.mutation
    def add_link(self, link_input: AddUrlLinkInput) -> UrlLinkType:
        with db.connection_context():
            new_link = UrlLink.create(
                url=link_input.url,
                title=link_input.title,
                collection_id=link_input.collection_id
            )
            return UrlLinkType(id=new_link.id, url=new_link.url, title=new_link.title, created_on=new_link.created_on, modified_on=new_link.modified_on)

    @strawberry.mutation
    def update_collection(self, collection_input: UpdateUrlsCollectionInput) -> Optional[UrlsCollectionType]:
        with db.connection_context():
            try:
                collection = UrlsCollection.get_by_id(collection_input.id)
                if collection_input.name is not None:
                    collection.name = collection_input.name
                if collection_input.description is not None:
                    collection.description = collection_input.description
                collection.modified_on = datetime.now()
                collection.save()
                return UrlsCollectionType(id=collection.id, name=collection.name, description=collection.description, created_on=collection.created_on, modified_on=collection.modified_on)
            except UrlsCollection.DoesNotExist:
                return None

    @strawberry.mutation
    def update_link(self, link_input: UpdateUrlLinkInput) -> Optional[UrlLinkType]:
        with db.connection_context():
            try:
                link = UrlLink.get_by_id(link_input.id)
                if link_input.url is not None:
                    link.url = link_input.url
                if link_input.title is not None:
                    link.title = link_input.title
                if link_input.collection_id is not None:
                    link.collection_id = link_input.collection_id
                link.modified_on = datetime.now()
                link.save()
                return UrlLinkType(id=link.id, url=link.url, title=link.title, created_on=link.created_on, modified_on=link.modified_on)
            except UrlLink.DoesNotExist:
                return None

    @strawberry.mutation
    def delete_collection(self, id: int) -> bool:
        with db.connection_context():
            try:
                collection = UrlsCollection.get_by_id(id)
                collection.delete_instance(recursive=True) # Deletes associated links
                return True
            except UrlsCollection.DoesNotExist:
                return False

    @strawberry.mutation
    def delete_link(self, id: int) -> bool:
        with db.connection_context():
            try:
                link = UrlLink.get_by_id(id)
                link.delete_instance()
                return True
            except UrlLink.DoesNotExist:
                return False

def get_app():
    schema = strawberry.Schema(query=Query, mutation=Mutation)
    graphql_app = GraphQLRouter(schema)

    app = FastAPI()
    app.include_router(graphql_app, prefix="/graphql")
    # uvicorn main:app --reload
    return app