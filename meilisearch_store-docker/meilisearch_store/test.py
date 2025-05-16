from database import get_db, Brand

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
    print("test success")

test()



