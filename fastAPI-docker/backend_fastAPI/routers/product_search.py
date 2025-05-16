from fastapi import APIRouter, Query
from meilisearch_python_async import Client

router_product_search = APIRouter()


async def perform_search(query):
    client = Client('http://172.22.0.3/16:7700', 'rcN6lh9xlE4_vcL7yuEK5YOrLleh8tdMR2m1FVcvRe0')
    index = client.index('product')
    print(index, query, '<<<<')
    result = await index.search(query=query, limit=5)
    return result


@router_product_search.get('/search/', tags=['search'])
async def search(query: str=Query(..., min_length=1)):
    print(query)
    result = await perform_search(query)
    return result
