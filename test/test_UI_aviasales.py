from pages.authPage import AuthPage
from pages.mainPage import MainPage

value_phone = "613922997"


def test_auth_by_phone(driver, PHONE_NUMBER):
    """ Авторизация по номеру телефона"""
    # Шаг1. Открываем главную страницу
    main_page = MainPage(driver)  # Создали экземпляр класса
    main_page.open(driver)
    # Кликаем на профиль
    main_page.click_profile()  # Перешли в окно авторизации по ноиеру телефона
    # Переходим к авторизации
    auth_page = AuthPage(driver)  # Создали экземпляр класса
    auth_page.click_enter()
    auth_page.choice_of_method()  # Выбираем вход по номеру телефона
    auth_page.enter_phone_number(PHONE_NUMBER)  # телефон вынести в файл .env и написать о нем в реадми





