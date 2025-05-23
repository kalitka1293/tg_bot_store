from fastapi import APIRouter, Query
from meilisearch import Client

router_product_search = APIRouter()


async def perform_search(query):
    client = Client('http://meilisearch:7700', 'rcN6lh9xlE4_vcL7yuEK5YOrLleh8tdMR2m1FVcvRe0')
    index = client.index('product')
    search_params = {
        "limit": 7,
    }
    result = index.search(query, search_params)
    return result


@router_product_search.get('/search/', tags=['search'])
async def search(query: str=Query(..., min_length=1)):
    print(query)
    result = await perform_search(query)
    return result
