import time
from api.cookie_manager import CookieManager

class AviasalesAPI:
    def __init__(self):
        self.cookie_mgr = CookieManager()
        self.base_url = "https://tickets-api.aviasales.ru"
        self.search_id = None
        self.last_request_id = None
    
    def _make_request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        
        if self.last_request_id:
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            kwargs['headers']['X-Request-Id'] = self.last_request_id
        
        response = self.cookie_mgr.request(method, url, **kwargs)
        
        if 'X-Request-Id' in response.headers:
            self.last_request_id = response.headers['X-Request-Id']
        
        return response
    
    def search_start(self, origin, destination, date_from, date_to, adults=1, children=0, infants=0):
        payload = {
            "search_params": {
                "directions": [
                    {
                        "origin": origin,
                        "destination": destination,
                        "date": date_from
                    },
                    {
                        "origin": destination,
                        "destination": origin,
                        "date": date_to
                    }
                ],
                "passengers": {
                    "adults": adults,
                    "children": children,
                    "infants": infants
                },
                "trip_class": "Y"
            },
            "marker": "direct",
            "market_code": "ru",
            "currency_code": "rub"
        }
        
        response = self._make_request('post', '/search/v2/start', json=payload)
        
        if response.status_code == 200:
            data = response.json()
            self.search_id = data.get('search_id')
            return self.search_id
        return None
    
    def search_one_way(self, origin, destination, date, adults=1, children=0, infants=0):
        payload = {
            "search_params": {
                "directions": [
                    {
                        "origin": origin,
                        "destination": destination,
                        "date": date
                    }
                ],
                "passengers": {
                    "adults": adults,
                    "children": children,
                    "infants": infants
                },
                "trip_class": "Y"
            },
            "marker": "direct",
            "market_code": "ru",
            "currency_code": "rub"
        }
        
        response = self._make_request('post', '/search/v2/start', json=payload)
        
        if response.status_code == 200:
            data = response.json()
            self.search_id = data.get('search_id')
            return self.search_id
        return None
    
    def search_result(self, search_id=None):
        if search_id:
            self.search_id = search_id
    
        if not self.search_id:
            return None
    
        current_timestamp = int(time.time())

        # Добавляем ожидание перед первым запросом
        print(f"\n Ждем 2 секунды перед первым запросом результатов...")
        time.sleep(2)
    
        payload = {
            "limit": 1,  # запрашиваем только 1 билет
            "price_per_person": False,
            "search_by_airport": False,
            "search_id": self.search_id,
            "last_update_timestamp": current_timestamp
        }
    
        print(f"\n Получаем результаты для search_id: {self.search_id}")
    
        for attempt in range(5):  # 5 попыток
            print(f"  Попытка {attempt + 1}/5...")
            response = self._make_request('post', '/search/v3.2/results', json=payload)
        
            if response.status_code == 200:
                data = response.json()
                # Проверяем, что data это список и он не пустой
                if data and len(data) > 0 and 'tickets' in data[0]:
                    tickets = data[0]['tickets']
                    print(f" Получено {len(tickets)} билетов")
                    return data
                
            elif response.status_code in [204, 304]:
                print(f" Результаты готовятся ({response.status_code})")
                time.sleep(2)
                continue
            else:
                print(f" Ошибка: {response.status_code}")
                print(f" Ответ: {response.text[:200]}")
                return None

        print(f" Превышено количество попыток")
        return None
    
