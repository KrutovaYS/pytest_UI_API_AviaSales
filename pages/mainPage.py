import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time # потом удалить
from datetime import datetime, timedelta


base_url = "https://www.aviasales.ru/"

class MainPage:
    """
    Класс для работы с главной страницей Aviasales.
    """
    COOKIE_ACCEPT_BUTTON = (By.XPATH, "//button[@data-test-id='accept-cookies-button']") # Локатор кнопки принятия куки
    ORIGIN_INPUT = (By.XPATH, "//input[@data-test-id='origin-input']")  # Откуда
    DESTINATION_INPUT = (By.XPATH, "//input[@data-test-id='destination-input']")  # Куда
    DATE_START = (By.XPATH, "//button[@data-test-id='start-date-field']")  # Дата вылета
    DATE_END = (By.CSS_SELECTOR, "[data-test-id='end-date-value']")  # Дата возвращения/прибытия
    SEARCH_BUTTON = (By.XPATH, "//button[@data-test-id='form-submit']")  # Кнопка поиска
    PASSENGERS_FIELD = (By.XPATH, "//button[@data-test-id='passengers-field']")  # Открыть меню с выбором количества пассажиров
    INFANTS_PLUS_BUTTON = (By.XPATH, "(//button[@data-test-id='increase-button'])[3]")  # Кнопка плюс добавление младенца
    # INFANTS_COINS = (By.XPATH, "(//div[@data-test-id='passenger-number'])")
    INFANTS_COUNS = (By.XPATH, "//div[@data-test-id='number-of-infants']//div[@data-test-id='passenger-number']")

    # Дополнительные локаторы для выпадающих списков
    DATE_CALENDAR = (By.XPATH, "//div[@data-test-id='dropdown']")  # выпадающий календарь для выбора дат вылета/прилета
    DATE_DAY_IN_CALENDAR = (By.XPATH, "//div[@data-test-id='date-19.03.2026']")  # дата вылета в календаре
    ORIGIN_SUGGEST = (By.XPATH, "//ul[@id='avia_form_origin-menu']")  #  Выпадающий список при вводе в поле Откуда
    DESTINATION_SUGGEST = (By.CSS_SELECTOR, "ul.suggest__list li:first-child")  # Выпадающий список при вводе в поле Куда
    PASSENGERS_INFO = (By.XPATH, "(//div[@data-test-id='trip-class-and-number-passengers'])[3]")  # Выпадающее меню с выбором количества пассажиров
    
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self) -> None:
        """ Открыть главную страницу
        Метод включает в себя открытие главной страницы, принятие куки
        """
        self.driver.get(base_url)
        # Ждем, пока страница загрузится (например, появится поле ввода)
        self.wait.until(
            EC.presence_of_element_located(self.SEARCH_BUTTON)
        )
        # Принимаем куки
        self.accept_cookies()

    def accept_cookies(self):
        """Принять куки, если есть баннер.
        Метод инициирует принятие куки ,нажав на кнопку "Да без проблем"
        """
        try:
            # Нажимаем на кнопку Да без проблем
            cookie_btn = self.wait.until(
                EC.element_to_be_clickable(self.COOKIE_ACCEPT_BUTTON)
            )
            cookie_btn.click()
        except:
            pass

        # Проверяем, что баннер куки исчез
        try:
            cookie_banner = self.driver.find_element(*self.COOKIE_ACCEPT_BUTTON)
            return not cookie_banner.is_displayed()
        except:
            return True  # Баннера нет - значит куки приняты

    def enter_origin(self, city: str) -> None:
        """ Ввести город вылета в поле Откуда"""
        # Ожидаем пока поле Откуда станет кликабельным
        origin_field = self.wait.until(
            EC.element_to_be_clickable(self.ORIGIN_INPUT)
        )

        # Ждем, пока автоподстановка по геолокации заполнит поле
        
        try:
            self.wait.until(
                lambda driver: origin_field.get_attribute('value') != ''
            )
            print("Автоподстановка сработала, поле заполнено")
        except:
            print("Автоподстановка не сработала ")

        # 3. Очищаем поле (несколько способов для надежности)
        origin_field.clear()  # Очистить поле
        origin_field.send_keys(Keys.CONTROL + 'a')  # выделить всё
        origin_field.send_keys(Keys.DELETE)  # удалить

        # 4. Вводим нужный город
        origin_field.send_keys(city)

        # Ждем появления выпадающего списка
        self.wait.until(EC.element_to_be_clickable(self.ORIGIN_SUGGEST))

         # Выбираем пункт с кодом VVO (Владивосток)
        try:
            # Ищем элемент с кодом VVO
            vvo_locator = (By.XPATH, "//li[contains(text(), 'VVO')]")
            vvo_option = self.wait.until(
                EC.element_to_be_clickable(vvo_locator)
            )
            vvo_option.click()
            print("Выбран Владивосток (VVO)")
        except:
            # Если не нашли VVO - первый пункт
            try:
                first_option = self.driver.find_element(*self.ORIGIN_SUGGEST)
                first_option.click()
            except:
                origin_field.send_keys(Keys.RETURN)

        # Получить значение из поля Откуда
        origin_field = self.wait.until(
            EC.presence_of_element_located(self.ORIGIN_INPUT)
        )
        assert origin_field.get_attribute('value') == city

    def enter_destination(self, city_destination):
        """Ввести город назначения."""
        dest_city = self.wait.until(
            EC.element_to_be_clickable(self.DESTINATION_INPUT)
        )
        dest_city.clear()
        dest_city.send_keys(city_destination)
        
        try:
            suggest = self.wait.until(
                EC.element_to_be_clickable(self.DESTINATION_SUGGEST)
            )
            suggest.click()
        except:
            # Пока используем Enter
            dest_city.send_keys(Keys.RETURN)

    def enter_date_start(self, start_date) -> str:
        date_start = self.wait.until(
            EC.element_to_be_clickable(self.DATE_START)
        )
        date_start.click()
        self.wait.until(EC.visibility_of_element_located(self.DATE_CALENDAR))
        # Ищем родительскую кнопку (более надежно)
        button_locator = (By.XPATH, f"//div[@data-test-id='date-{start_date}']/ancestor::button")
        day_button = self.wait.until(
            EC.element_to_be_clickable(button_locator)
        )
        
        day_button.click()
        # Получить значение даты вылета
        date_field = self.wait.until(
            EC.presence_of_element_located(self.DATE_START)
        )
        return date_field.text

    def enter_date_end(self, end_date) -> str:
        """ Ввести дату прибытия"""
        date_end = self.wait.until(
            EC.element_to_be_clickable(self.DATE_END)
        )
        date_end.click()
        self.wait.until(EC.visibility_of_element_located(self.DATE_CALENDAR))
        DATE_BUTTON_LOCATOR = (By.XPATH, f"//div[@data-test-id='date-{end_date}']/ancestor::button")
        day_button = self.wait.until(
            EC.element_to_be_clickable(DATE_BUTTON_LOCATOR)
        )
        day_button.click()

        # Получить значение даты возвращения
        date_field = self.wait.until(
            EC.presence_of_element_located(self.DATE_END)
        )
        return date_field.text

    def enter_search_btn(self):
        """ Нажать кнопку поиска билетов. """
        search_btn = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_BUTTON)
        )
        search_btn.click()

        WebDriverWait(self.driver, 20).until(
            lambda d: any(s in d.current_url for s in ("search", "params=", "aviasales")),
            message="URL не обновился до страницы поиска/результатов за 20 с",
        )

        # Проверить,что url теперь содержит "search"
        current_url = self.driver.current_url
        assert (
            "search" in current_url or "aviasales" in current_url or "params=" in current_url
        ), "Ожидалась страница поиска или главная"

        self.switch_to_results_tab()
        
    def switch_to_results_tab(self):
        """Переключиться на вкладку с результатами"""
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])

    def add_infant(self) -> str:
        """ Добавить младенца в параметры поиска
        Returns: текст с информацией о пассажирах
        """
        # 1. Открываем меню выбора пассажиров
        passengers_field = self.wait.until(
            EC.element_to_be_clickable(self.PASSENGERS_FIELD)
        )
        passengers_field.click()

        # Нажимаем на кнопку + для младенцев
        infant_plus = self.wait.until(
            EC.element_to_be_clickable(self.INFANTS_PLUS_BUTTON)
        )
        infant_plus.click()

        # Проверяем, что количество младенцев стало 1
        passenger_info = self.wait.until(
            EC.visibility_of_element_located(self.INFANTS_COUNS)
        )
        passenger_text = passenger_info.text

        # Закрываем меню пассажиров (клик вне меню)
        self.driver.find_element(By.TAG_NAME, "body").click()

        return passenger_text
    
    
