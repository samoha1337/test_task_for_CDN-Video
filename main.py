from fastapi import FastAPI, HTTPException
from schemas import CityCreate, CityResponse
from city_service import add_city, delete_city, get_all_cities, find_nearest_cities

app = FastAPI()

# Маршрут для добавления нового города
@app.post("/cities/", response_model=CityResponse)
async def create_city(city: CityCreate):
    try:
        # Добавляем город и получаем информацию о нем
        city_data = add_city(city.name) 
        
        if city_data is None:
            raise HTTPException(status_code=400, detail="Failed to get coordinates for the city.")
        
        return CityResponse(
            id=city_data['id'],
            name=city_data['name'],
            latitude=city_data['latitude'],
            longitude=city_data['longitude']
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Маршрут для удаления города по его ID
@app.delete("/cities/{city_id}", response_model=dict)
def remove_city(city_id: int):
    try:
        delete_city(city_id) 
        return {"detail": "City deleted successfully."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Маршрут для получения информации о всех городах
@app.get("/cities/", response_model=list[CityResponse])
def read_cities():
    try:
        cities = get_all_cities() 
        return cities
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Маршрут для поиска двух ближайших городов к заданной точке
@app.get("/cities/nearest/", response_model=list[CityResponse])
def get_nearest_cities(latitude: float, longitude: float):
    try:
        nearest_cities = find_nearest_cities(latitude, longitude) 
        return nearest_cities
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
