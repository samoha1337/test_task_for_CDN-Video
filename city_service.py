import requests
import math
from database import get_db_connection

# Функция для получения координат города через внешний API
def get_city_coordinates(city_name: str):
    api_key = '492ac03b-bd25-4feb-8449-10d79d6e72ae'
    response = requests.get(f"https://catalog.api.2gis.ru/3.0/items/geocode?key={api_key}&fields=items.point&q={city_name}")     
    data = response.json()

    # Проверяем, что 'result' и 'items' присутствуют и не пусты
    if 'result' not in data or 'items' not in data['result'] or len(data['result']['items']) == 0:
        raise KeyError("'items' not found in the response data or empty")

    item = data['result']['items'][0]
    if 'point' not in item:
        raise KeyError("'point' not found in the item data")

    lat = item['point'].get('lat')
    lon = item['point'].get('lon')
    if lat is None or lon is None:
        raise KeyError("Latitude or longitude not found in the point data")

    return lat, lon

# Добавление нового города в БД
def add_city(city_name: str):
    latitude, longitude = get_city_coordinates(city_name)
    if latitude is None or longitude is None:
        return None

    conn = get_db_connection()
    cursor = conn.cursor()  # Создаем курсор
    cursor.execute(
        'INSERT INTO cities (name, latitude, longitude) VALUES (?, ?, ?)',
        (city_name, latitude, longitude)
    )
    conn.commit()

    # Получаем ID последней вставленной строки
    city_id = cursor.lastrowid

    conn.close()

    return {
        'id': city_id,
        'name': city_name,
        'latitude': latitude,
        'longitude': longitude
    }

# Функция для удаления города из базы данных по его ID
def delete_city(city_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cities WHERE id = ?', (city_id,))
    conn.commit()
    conn.close()

# Функция для получения списка всех городов из базы данных
def get_all_cities():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cities')
    cities = cursor.fetchall()
    conn.close()
    return [
        {
            'id': city['id'],
            'name': city['name'],
            'latitude': city['latitude'],
            'longitude': city['longitude']
        }
        for city in cities
    ]

# Функция для расчета расстояния между двумя точками (в километрах)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Радиус Земли в километрах
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    # Используем формулу Гаверсинуса для определения расстояния между точками
    a = (math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

# Функция для нахождения двух ближайших городов к заданной точке (latitude, longitude)
def find_nearest_cities(latitude: float, longitude: float):
    cities = get_all_cities()
    cities.sort(key=lambda city: haversine(latitude, longitude, city['latitude'], city['longitude']))
    return cities[:2]
