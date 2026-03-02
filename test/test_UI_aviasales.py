import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from pages.resultPage import ResultPage
from pages.mainPage import MainPage
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

    main_page.switch_to_results_tab()  #Переходим на вкладку результатов
    
    # Ждём загрузки результатов, чтобы не вызывать find_element пока страница ещё грузится
    result_page.wait_for_results_ready(timeout=45)
    # Проверяем первую цену
    first_price = result_page.get_first_price()
    assert first_price, "Цена первого билета не найдена"
    assert result_page.is_price_valid(first_price), f"Цена не похожа на число: '{first_price}'"

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

    main_page.switch_to_results_tab()  #Переходим на вкладку результатов

    result_page.wait_for_results_ready(timeout=40)  # 
    # Проверяем первую цену
    first_price = result_page.get_first_price()
    assert first_price, "Цена первого билета не найдена"
    assert result_page.is_price_valid(first_price), f"Цена не похожа на число: '{first_price}'"
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

    # Шаг 4. Проверяем сценарий «нет билетов»
    assert result_page.has_no_results(), (
        "Ожидалось сообщение об отсутствии билетов или пустой список результатов"
    )

def test_add_to_like(driver):
    """ Тест на добавление в Избранное (без авторизации)"""
    result_page = ResultPage(driver)
    login_form_text = result_page.add_to_favourite_without_auth()

    assert login_form_text == "Войдите в профиль"

def test_search_tickets_with_infant(driver: WebDriver):
    """ Тест на поиск билетов с младенцем (Владивосток - Сочи, 19.03-20.03.2026, 1 взрослый + 1 младенец)"""
    
    # Шаг 1. Открываем главную страницу
    main_page = MainPage(driver)
    result_page = ResultPage(driver)
    main_page.open()
    
    # Шаг 2. Вводим города и даты
    main_page.enter_origin('Владивосток')
    main_page.enter_destination('Сочи')
    main_page.enter_date_start('19.03.2026')
    main_page.enter_date_end('20.03.2026')
    
    # Шаг 3. Добавляем младенца через метод
    infant_text = main_page.add_infant()

    # Проверяем, что младенец добавился (значение "1")
    assert infant_text == "1", f"Ожидалось количество младенцев 1, получено: {infant_text}"
    print("✅ Младенец успешно добавлен")
    
    # Шаг 5. Выполняем поиск
    main_page.enter_search_btn()
    
    # Шаг 6. Проверяем результаты
    result_page.wait_for_results_ready(timeout=45)
    
    # Проверяем первую цену
    first_price = result_page.get_first_price()
    assert first_price, "Цена первого билета не найдена"
    assert result_page.is_price_valid(first_price), f"Цена не похожа на число: '{first_price}'"
    print(f"💰 Цена первого билета: {first_price}")
    
    print("\n✅ Тест на поиск билетов с младенцем успешно пройден!")


    




