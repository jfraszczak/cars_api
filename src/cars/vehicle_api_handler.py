import requests
from abc import ABC, abstractmethod


class VehicleAPIHandlerInterface(ABC):

    @abstractmethod
    def get_valid_vehicle(self, make: str, model: str) -> tuple[str, str] | None:
        '''
        Returns make and name of the vehicle as specified in Vehicle API,
        if such vehicle exists, otherwise returns None.
        '''
        pass


class VehicleAPIHandler(VehicleAPIHandlerInterface):

    def _get_models(self, make: str) -> dict[int, str, int, str]:
        request = 'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{}?format=json'.format(make)
        response = requests.get(request)
        results = response.json()['Results']
        return results

    def get_valid_vehicle(self, make: str, model: str) -> tuple[str, str] | None:
        results = self._get_models(make)
        for result in results:
            if result['Model_Name'].lower() == model.lower(): # case insensitive
                return (result['Make_Name'], result['Model_Name'])

        return None
