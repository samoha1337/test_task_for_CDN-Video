from pydantic import BaseModel

# Модель для создания нового города, принимающая только название города.
class CityCreate(BaseModel):
    name: str

# Модель для представления данных о городе
class CityResponse(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    
    #Метод класса для создания объекта CityResponse из данных внешнего API 
    @classmethod
    def from_api_data(cls, api_data):
         # Извлечение первого элемента из списка 'items'
        item = api_data['result']['items'][0]
        # Возврат нового объекта CityResponse, созданного из данных item
        return cls(
            id=item['id'],
            name=item['name'],
            latitude=item['point']['lat'],
            longitude=item['point']['lon']
        )
