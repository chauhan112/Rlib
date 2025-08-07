from typing import List, Optional
from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter

from .db import Job, JobCV, MotivationCV, db
from datetime import datetime
from peewee import IntegrityError

# --- GraphQL Types ---

@strawberry.type
class JobType:
    id: int
    created_on: datetime
    modified_on: datetime
    title: str
    description: str
    summary: str
    link: str

    @classmethod
    def from_instance(cls, model: Job):
        return cls(
            id=model.id,
            created_on=model.created_on.isoformat(),
            modified_on=model.modified_on.isoformat(),
            title=model.title,
            description=model.description,
            summary=model.summary,
            link=model.link
        )

    @property
    def motivations(self):
        return [MotivationCVType.from_instance(mot) for mot in MotivationCV.select().where(MotivationCV.job_id == self.id)]

    @property
    def cv(self):
        return JobCVType.from_instance(JobCV.get_or_none(JobCV.job_id == self.id))
@strawberry.type
class JobCVType:
    id: int
    created_on: datetime
    modified_on: datetime
    content: str
    all_content: str 

    @classmethod
    def from_instance(cls, model: JobCV):
        return cls(
            id=model.id,
            created_on=model.created_on.isoformat(),
            modified_on=model.modified_on.isoformat(),
            content=model.content,
            all_content=model.all_content
        )
MotivationCVType = JobCVType

@strawberry.type
class Query:
    @strawberry.field
    def read_all_jobs(self) -> List[JobType]:
        with db.connection_context():
            return [JobType.from_instance(col) for col in Job.select()]

    @strawberry.field
    def read_job(self, id: int) -> Optional[JobType]:
        with db.connection_context():
            collection = Job.get_or_none(Job.id == id)
            if collection:
                return Job.from_instance(collection)
            return None

    @strawberry.field
    def read_all_jobcv(self) -> List[JobCVType]:
        with db.connection_context():
            return [JobCVType.from_instance(col) for col in JobCV.select()]

    @strawberry.field
    def read_jobcv(self, id: int) -> Optional[JobCVType]:
        with db.connection_context():
            collection = JobCV.get_or_none(JobCV.id == id)
            if collection:
                return JobCV.from_instance(collection)
            return None
    @strawberry.field
    def read_all_motivations(self) -> List[JobCVType]:
        with db.connection_context():
            return [JobCVType.from_instance(col) for col in JobCVType.select()]

    @strawberry.field
    def read_motivation(self, id: int) -> Optional[JobCVType]:
        with db.connection_context():
            collection = JobCVType.get_or_none(JobCVType.id == id)
            if collection:
                return JobCVType.from_instance(collection)
            return None

# # --- Mutations ---

# @strawberry.type
# class Mutation:
#     @strawberry.mutation
#     def add_collection(self, collection_input: AddUrlsCollectionInput) -> UrlsCollectionType:
#         with db.connection_context():
#             try:
#                 new_collection = UrlsCollection.create(
#                     name=collection_input.name,
#                     description=collection_input.description
#                 )
#                 return UrlsCollectionType.from_instance(new_collection)
#             except IntegrityError:
#                 raise Exception("A collection with this name already exists.")

#     @strawberry.mutation
#     def add_link(self, link_input: AddUrlLinkInput) -> UrlLinkType:
#         with db.connection_context():
#             new_link = UrlLink.create(url=link_input.url, title=link_input.title, collection_id=link_input.collectionId)
#             return UrlLinkType.from_instance(new_link)

#     @strawberry.mutation
#     def update_collection(self, collection_input: UpdateUrlsCollectionInput) -> Optional[UrlsCollectionType]:
#         with db.connection_context():
#             try:
#                 collection = UrlsCollection.get_by_id(collection_input.id)
#                 if collection_input.name is not None:
#                     collection.name = collection_input.name
#                 if collection_input.description is not None:
#                     collection.description = collection_input.description
#                 collection.modified_on = datetime.now()
#                 collection.save()
#                 return UrlsCollectionType.from_instance(collection)
#             except UrlsCollection.DoesNotExist:
#                 return None

#     @strawberry.mutation
#     def update_link(self, link_input: UpdateUrlLinkInput) -> Optional[UrlLinkType]:
#         with db.connection_context():
#             try:
#                 link = UrlLink.get_by_id(link_input.id)
#                 if link_input.url is not None:
#                     link.url = link_input.url
#                 if link_input.title is not None:
#                     link.title = link_input.title
#                 if link_input.collectionId is not None:
#                     link.collection_id = link_input.collectionId
#                 link.modified_on = datetime.now()
#                 link.save()
#                 return UrlLinkType.from_instance(link)
#             except UrlLink.DoesNotExist:
#                 return None

#     @strawberry.mutation
#     def delete_collection(self, id: int) -> bool:
#         with db.connection_context():
#             try:
#                 collection = UrlsCollection.get_by_id(id)
#                 collection.delete_instance(recursive=True) # Deletes associated links
#                 return True
#             except UrlsCollection.DoesNotExist:
#                 return False

#     @strawberry.mutation
#     def delete_link(self, id: int) -> bool:
#         with db.connection_context():
#             try:
#                 link = UrlLink.get_by_id(id)
#                 link.delete_instance()
#                 return True
#             except UrlLink.DoesNotExist:
#                 return False

def get_graphql_app():
    schema = strawberry.Schema(query=Query, mutation=Mutation)
    graphql_app = GraphQLRouter(schema)

    return graphql_app
def get_app():
    app = FastAPI()
    app.include_router(get_graphql_app(), prefix="/graphql")
    # uvicorn main:app --reload
    return app