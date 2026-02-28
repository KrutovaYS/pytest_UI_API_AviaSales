import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from pages.resultPage import ResultPage
from pages.mainPage import MainPage
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_search_tickets(driver: WebDriver):
    """ Тест на поиск билетов на конкретные даты без авторизации"""
    # Шаг 1. Открываем главную страницу
    main_page = MainPage(driver)  # Создали экземпляр класса
    result_page = ResultPage(driver)
    main_page.open()

    # Шаг 2. Вводим поисковые параметры: город Откуда, город Куда, дата вылета, дата прибытия
    main_page.enter_origin('Владивосток')
    main_page.enter_destination('Самара')
    main_page.enter_date_start('19.03.2026')
    main_page.enter_date_end('20.03.2026')

    # Шаг 3. Нажимаем кнопку Найти билеты
    main_page.enter_search_btn()

    # Проверяем, что мы перешли на страницу результатов
    current_url = driver.current_url
    assert "search" in current_url or "results" in current_url, "Не перешли на страницу результатов!"

    # Проверяем первую цену
    first_price = result_page.get_first_price()
    assert first_price, "Цена первого билета не найдена"
    print(f"Цена первого билета: {first_price}")

    print("\n Тест успешно пройден! Все проверки выполнены.")

def test_ticket_in_one_way(driver: WebDriver):
    """ Тест на поиск билетов в один конец"""
    # Шаг 1. Открываем главную страницу
    main_page = MainPage(driver)  # Создали экземпляр класса
    result_page = ResultPage(driver)
    main_page.open()

    # Шаг 2. Вводим поисковые параметры: город Откуда, город Куда, дата вылета, дата прибытия
    main_page.enter_origin('Владивосток')
    main_page.enter_destination('Сочи')
    main_page.enter_date_start('19.03.2026')

    # Шаг 3. Нажимаем кнопку Найти билеты
    main_page.enter_search_btn()

    # Проверяем первую цену
    first_price = result_page.get_first_price()
    assert first_price, "Цена первого билета не найдена"
    print(f"Цена первого билета: {first_price}")

def test_duble_city(driver: WebDriver):
    """ Тест на поиск с дублированием города Откуда и Куда"""
    # Шаг 1. Открываем главную страницу
    main_page = MainPage(driver)  # Создали экземпляр класса
    result_page = ResultPage(driver)
    main_page.open()

    # Шаг 2. Вводим поисковые параметры: город Откуда, город Куда, дата вылета, дата прибытия
    main_page.enter_origin('Владивосток')
    main_page.enter_destination('Владивосток')
    main_page.enter_date_start('19.03.2026')
    main_page.enter_date_end('20.03.2026')
    
    # Шаг 3. Нажимаем кнопку Найти билеты
    main_page.enter_search_btn()

    # Шаг 4. Проверяем результат поиска
    

def test_add_to_like(driver):
    """ Тест на добавление в Избранное (без авторизации)"""
    # Шаг 1. Сначала выполним поиск билетов
    main_page = MainPage(driver)  # Создали экземпляр класса
    main_page.open()
    main_page.enter_origin('Самара')
    main_page.enter_destination('Сочи')
    main_page.enter_date_start('19.03.2026')
    main_page.enter_date_end('20.03.2026')
    
    main_page.enter_search_btn()

    # Шаг 2. На странице результата нажимаем значок сердца(Добавить в Избранное)


# def test_date_period_more_year(driver):
#     """Тест на проверку выбора дат с промежутком в несколько месяцев"""


# def test_search_tickets_with_auth(driver_with_auth):
#     """ Тест на поиск билетов с авторизацией"""
    
#     main_page = MainPage(driver_with_auth)
    
#     # ШАГ 1: Открываем страницу и проверяем куки
#     main_page.open()  

#     # Проверка 1: Куки приняты
#     assert main_page.are_cookies_accepted(), "Куки не были приняты"

#     # Проверка 2: Добавлены мои куки авторизации
#     guest_cookie = main_page.get_cookie_value("_guestia_key")
    
#     assert guest_cookie is not None, "Кука _guestia_key не найдена"
#     print(f"✓ Кука авторизации найдена: {guest_cookie['value'][:20]}...")

#      # ШАГ 2: Вводим поисковые параметры
#     test_data = {
#         'origin': 'Владивосток',
#         'destination': 'Сочи',
#         'start_date': '19.03.2026',
#         'end_date': '20.03.2026'
#     }
    
#     main_page.enter_origin(test_data['origin'])
#     main_page.enter_destination(test_data['destination'])
#     main_page.enter_date_start(test_data['start_date'])
#     main_page.enter_date_end(test_data['end_date'])
    
#     # Проверка 3: Поле Откуда содержит правильный город
#     origin_value = main_page.get_origin_value()
#     assert 'Владивосток' in origin_value or 'VVO' in origin_value, \
#         f"В поле Откуда ожидался Владивосток, но получено: {origin_value}"
#     print(f"✓ Поле Откуда: {origin_value}")
    
#     # Проверка 4: Поле Куда содержит правильный город
#     dest_value = main_page.get_destination_value()
#     assert 'Сочи' in dest_value or 'AER' in dest_value, \
#         f"В поле Куда ожидался Сочи, но получено: {dest_value}"
#     print(f"✓ Поле Куда: {dest_value}")
    
#     # Проверка 5: Поле Когда содержит выбранную дату
#     start_date_value = main_page.get_start_date_value()
#     assert '19' in start_date_value and 'мар' in start_date_value, \
#         f"Дата вылета не соответствует: {start_date_value}"
#     print(f"✓ Дата вылета: {start_date_value}")
    
#     # Проверка 6: Поле Обратно содержит выбранную дату
#     end_date_value = main_page.get_end_date_value()
#     assert '20' in end_date_value and 'мар' in end_date_value, \
#         f"Дата возвращения не соответствует: {end_date_value}"
#     print(f"✓ Дата возвращения: {end_date_value}")
  
#      # ШАГ 3: Нажимаем кнопку поиска
#     main_page.enter_search_btn()
#     sleep(50)
    
   



    




