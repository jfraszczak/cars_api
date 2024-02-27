import pytest
from ...src.cars.db_handler import DBHandler, CarAttribute

db_handler = DBHandler('ai_clearing', 'cars_test')
db_handler.reset()

def test_insert_car():
    assert db_handler.car_exists('make1', 'model1') == False
    assert db_handler.car_exists('make2', 'model2') == False

    db_handler.insert_car('make1', 'model1')
    assert db_handler.car_exists('make1', 'model1') == True

    with pytest.raises(Exception) as e:
        db_handler.insert_car('make1', 'model1')

    db_handler.insert_car('make2', 'model2')
    assert db_handler.car_exists('make1', 'model1') == True
    assert db_handler.car_exists('make2', 'model2') == True
    db_handler.reset()

def test_update_rate():
    db_handler.insert_car('make1', 'model1')

    db_handler.update_rate('make1', 'model1', 4)
    record = db_handler.get_car('make1', 'model1')
    assert record[CarAttribute.RATES_SUM.value] == 4
    assert record[CarAttribute.RATES_NUM.value] == 1

    db_handler.update_rate('make1', 'model1', 3)
    record = db_handler.get_car('make1', 'model1')
    assert record[CarAttribute.RATES_SUM.value] == 7
    assert record[CarAttribute.RATES_NUM.value] == 2

    db_handler.update_rate('make1', 'model1', 1)
    record = db_handler.get_car('make1', 'model1')
    assert record[CarAttribute.RATES_SUM.value] == 8
    assert record[CarAttribute.RATES_NUM.value] == 3
    db_handler.reset()

def test_get_all_cars():
    result = db_handler.get_all_cars()
    assert len(result) == 0

    db_handler.insert_car('make1', 'model1')
    db_handler.update_rate('make1', 'model1', 4)
    db_handler.update_rate('make1', 'model1', 2)
    result = db_handler.get_all_cars()
    assert result[0]['rate_avg'] == 3

    db_handler.insert_car('make2', 'model2')
    db_handler.insert_car('make3', 'model3')
    result = db_handler.get_all_cars()
    assert len(result) == 3
    db_handler.reset()

def test_get_popular_cars():
    db_handler.insert_car('make1', 'model1')
    db_handler.insert_car('make2', 'model2')
    db_handler.insert_car('make3', 'model3')

    for _ in range(10):
        db_handler.update_rate('make3', 'model3', 4)

    for _ in range(5):
        db_handler.update_rate('make1', 'model1', 4)

    for _ in range(2):
        db_handler.update_rate('make2', 'model2', 4)
    
    result = db_handler.get_popular_cars(2)
    assert len(result) == 2
    result[0][CarAttribute.MAKE.value] == 'make3'
    result[1][CarAttribute.MAKE.value] == 'make1'
    db_handler.reset()
