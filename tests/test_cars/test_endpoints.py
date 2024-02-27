from fastapi.testclient import TestClient
from ...src.cars.db_handler import DBHandler
from ...src.cars.router import get_db_handler
from ...src.cars.vehicle_api_handler import VehicleAPIHandlerInterface, VehicleAPIHandler
from ...src.main import app

def get_test_db_handler() -> DBHandler:
    db_handler = DBHandler('ai_clearing', 'cars_test')
    db_handler.reset()
    for i in range(1, 101):
        db_handler.insert_car('make{}'.format(i), 'model{}'.format(i))
    
    return db_handler

class TestVehicleAPIHandler(VehicleAPIHandlerInterface):

    def get_valid_vehicle(self, make: str, model: str) -> tuple[str, str] | None:
        if make[:4] == 'make' and model[:5] == 'model':
            return (make, model)
        return None

app.dependency_overrides[get_db_handler] = get_test_db_handler
app.dependency_overrides[VehicleAPIHandler] = TestVehicleAPIHandler
client = TestClient(app)

def test_post_cars():
    response = client.post(
        '/cars',
        json={"make": "make1", "model": "model1"}
    )
    assert response.status_code == 400

    response = client.post(
        '/cars',
        json={"make": "make101", "model": "model101"}
    )
    assert response.status_code == 200

    response = client.post(
        '/cars',
        json={"make": "dadas", "model": "gdgds"}
    )
    assert response.status_code == 400

def test_post_rate():
    response = client.post(
        '/rate',
        json={"make": "make1", "model": "model1", "rate": 5}
    )
    assert response.status_code == 200

    response = client.post(
        '/rate',
        json={"make": "make1", "model": "model1", "rate": 6}
    )
    assert response.status_code == 422

    response = client.post(
        '/rate',
        json={"make": "make1", "model": "model1", "rate": 2.5}
    )
    assert response.status_code == 422

    response = client.post(
        '/rate',
        json={"make": "make1", "model": "model1", "rate": 0}
    )
    assert response.status_code == 422

    response = client.post(
        '/rate',
        json={"make": "make200", "model": "model200", "rate": 5}
    )
    assert response.status_code == 400

def test_get_cars():
    response = client.get('/cars')
    assert response.status_code == 200

def test_get_popular():
    response = client.get('/popular?top_n=3')
    assert response.status_code == 200

    response = client.get('/popular?top_n=-1')
    assert response.status_code == 422

    response = client.get('/popular?top_n=0')
    assert response.status_code == 422

    response = client.get('/popular?top_n=1.3')
    assert response.status_code == 422
