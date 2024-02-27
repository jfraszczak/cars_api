from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Annotated
from .schemas import Car, CarRate
from .db_handler import DBHandler
from .vehicle_api_handler import VehicleAPIHandler, VehicleAPIHandlerInterface

router = APIRouter()

def get_db_handler() -> DBHandler:
    return DBHandler('ai_clearing', 'cars')

@router.post("/cars")
async def post_cars(car: Car, db_handler: DBHandler=Depends(get_db_handler), vehicle_api_handler: VehicleAPIHandlerInterface=Depends(VehicleAPIHandler)):
    vehicle = vehicle_api_handler.get_valid_vehicle(car.make, car.model)
    if vehicle is None:
        raise HTTPException(status_code=400, detail="Specified vehicle does not exist")

    try:
        db_handler.insert_car(*vehicle)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return car
    
@router.post("/rate")
async def post_rate(car_rate: CarRate, db_handler=Depends(get_db_handler), vehicle_api_handler: VehicleAPIHandlerInterface=Depends(VehicleAPIHandler)):
    try:
        make, model = vehicle_api_handler.get_valid_vehicle(car_rate.make, car_rate.model)
        db_handler.update_rate(make, model, car_rate.rate)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return car_rate

@router.get("/cars")
async def get_cars(db_handler=Depends(get_db_handler)):
    try: 
        return db_handler.get_all_cars()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/popular")
async def get_cars(top_n: Annotated[int, Query(ge=1)], db_handler=Depends(get_db_handler)):
    try: 
        return db_handler.get_popular_cars(top_n)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
