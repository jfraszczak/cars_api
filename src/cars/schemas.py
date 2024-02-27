from pydantic import BaseModel, Field


class Car(BaseModel):
    make: str
    model: str

class CarRate(Car):
    rate: int = Field(ge=1, le=5)
