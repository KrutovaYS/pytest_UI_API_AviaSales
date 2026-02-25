import pytest
from api.aviasales_api import AviasalesAPI

def test_search_specific_dates():
    """Тест 1: Поиск билетов на конкретные даты"""
    api = AviasalesAPI()
    
    search_id = api.search_start(
        origin='KUF',
        destination='AER',
        date_from='2026-11-08',
        date_to='2026-11-09',
        adults=1
    )
    
    assert search_id is not None
    
    # Запрос на получение результата по search_id
    results = api.search_result(search_id)
    assert results is not None

def test_search_one_way():
    """Тест 2: Поиск билета в один конец"""
    api = AviasalesAPI()
    
    search_id = api.search_one_way(
        origin='KUF',
        destination='AER',
        date='2026-11-08',
        adults=1
    )
    
    assert search_id is not None

    # Запрос на получение результата по search_id
    results = api.search_result(search_id)
    assert results is not None

def test_search_several_months():
    """Тест 3: Поиск с диапазоном в несколько месяцев"""
    api = AviasalesAPI()
    
    search_id = api.search_start(
        origin='KUF',
        destination='AER',
        date_from='2026-11-08',
        date_to='2027-02-08',
        adults=1
    )
    
    assert search_id is not None

    # Запрос на получение результата по search_id
    results = api.search_result(search_id)
    assert results is not None

def test_search_with_infant():
    """Тест 4: Поиск с 1 взрослым и 1 младенцем"""
    api = AviasalesAPI()
    
    search_id = api.search_start(
        origin='KUF',
        destination='AER',
        date_from='2026-11-08',
        date_to='2026-11-09',
        adults=1,
        infants=1
    )
    
    # Запрос на получение результата по search_id
    results = api.search_result(search_id)
    assert results is not None

def test_duplicate_city():
    """Тест 5: Дублирование города"""
    api = AviasalesAPI()
    
    search_id = api.search_start(
        origin='KUF',
        destination='KUF',
        date_from='2026-11-08',
        date_to='2026-11-09',
        adults=1
    )
    
    assert search_id is None
