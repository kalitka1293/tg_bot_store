from database import get_product_data_meilisearch, get_all_product_data_meilisearch
from app import client

def add_all_data_product(index: str):
    document = get_all_product_data_meilisearch()
    print(document, type(document), 'document')
    if document is None:
        print('база данных пустая')
        return
    client.index(index).add_documents(document)

def add_one_data_product(index: str, product_id: int):
    document = get_product_data_meilisearch(product_id)
    result = client.index(index).add_documents(document)
    print(result)

# add_all_data_product('product')
