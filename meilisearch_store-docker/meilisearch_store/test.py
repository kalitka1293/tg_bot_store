from database import get_db, Brand
from dowload_data_meilisearch import add_all_data_product
from app import client
def test():
    print("Run test!")
    db = get_db()
    test_data = Brand(brand='TEST_NAME')
    db.add(test_data)
    db.commit()
    db.refresh(test_data)  # Обновляем объект, чтобы получить id из БД

    result_id = test_data.id

    # Получаем объект по id
    brand_from_db = db.get(Brand, result_id)

    # Можно проверить, что объект найден
    if brand_from_db is None:
        raise Exception(f"Brand с id={result_id} не найден")

    # Удаляем объект
    db.delete(brand_from_db)
    db.commit()
    print("test BD success")
    # print('update_searchable_attributes')
    # index = client.index('product')
    # response = index.update_searchable_attributes([
    #     "name",
    #     "description",
    #     "brand",
    #     "country",
    #     "group_product",
    #     "type_equipment"
    # ])
    # print('Update response:', response)
    print('TEST download data bd in meilisearch')
    add_all_data_product('product')
    print('Success')

    print('test get data meilisearch')
    res = client.index('product')
    c = res.search('test')
    print(c, '<<<')
test()



