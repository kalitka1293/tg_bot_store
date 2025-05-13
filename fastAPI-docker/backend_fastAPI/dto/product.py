from pydantic import BaseModel


class Meilisearch(BaseModel):
    query: str
