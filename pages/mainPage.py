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
    ORIGIN_INPUT = (By.CSS_SELECTOR, "[data-test-id='origin-input']")  # Откуда
    DESTINATION_INPUT = (By.CSS_SELECTOR, "[data-test-id='destination-input']")  # Куда
    DATE_START = (By.CSS_SELECTOR, "[data-test-id='start-date-value']")  # Дата вылета
    DATE_END = (By.CSS_SELECTOR, "[data-test-id='end-date-value']")  # Дата возвращения/прибытия
    SEARCH_BUTTON = (By.XPATH, "//button[@data-test-id='form-submit']")  # Кнопка поиска
    
    # Дополнительные локаторы для выпадающих списков
    ORIGIN_SUGGEST = (By.CSS_SELECTOR, "[data-test-id='origin-suggest'] li:first-child")
    DESTINATION_SUGGEST = (By.CSS_SELECTOR, "[data-test-id='destination-suggest'] li:first-child")

     # Локатор кнопки принятия куки (на основе скриншота)
    COOKIE_ACCEPT_BUTTON = (By.XPATH, "//button[@data-test-id='accept-cookies-button']")

    

    def __init__(self, __driver) -> None:
        self.__driver = __driver
        self.wait = WebDriverWait(__driver, 10)

    def open(self, __driver: WebDriver):
        """ Открыть главную страницу"""
        self.__driver.get(base_url)
        # Ждем, пока страница загрузится (например, появится поле ввода)
        self.wait.until(
            EC.presence_of_element_located(self.SEARCH_BUTTON)
        )
        # Сразу принимаем куки
        self.accept_cookies()

    def accept_cookies(self):
        """Принять куки, если есть баннер."""
        try:
            # Пробуем найти кнопку принятия куки в течение 3 секунд
            cookie_btn = self.wait.until(
                EC.element_to_be_clickable(self.COOKIE_ACCEPT_BUTTON)
            )
            cookie_btn.click()
        except:
            pass

    # Нажать кнопку(значок) профиля
    def click_profile(self):           
        btn_profile = self.__driver.find(By.XPATH, "//button[@data-test-id='profile-button']")
        btn_profile.click()

        assert self.__driver.find.element(By.XPATH, "//div[@data-test-id='dropdown']")



    # def enter_origin(self, city):
    #     """ Ввести город вылета"""
    #     element = self.__driver.find_element(self.ORIGIN_INPUT)
    #     element.clear()
    #     element.send_keys(city)
    #     # Ждем появления выпадающего списка
    #     try:
    #         suggest = self.wait.until(
    #             EC.element_to_be_clickable(self.ORIGIN_SUGGEST),
    #         )
    #         suggest.click()
    #     except:
    #         element.send_keys(Keys.RETURN)

    # def enter_destination(self, city):
    #     """Ввести город назначения."""
    #     dest_field = self.wait.until(
    #         EC.element_to_be_clickable(self.DESTINATION_INPUT)
    #     )
    #     dest_field.clear()
    #     dest_field.send_keys(city)
        
    #     try:
    #         suggest = self.wait.until(
    #             EC.element_to_be_clickable(self.DESTINATION_SUGGEST),
    #         )
    #         suggest.click()
    #     except:
    #         dest_field.send_keys(Keys.RETURN)
        
    # def select_dates(self, days_from_now=7, trip_days=7):
    #     """
    #     Выбор дат вылета и возвращения.
        
    #     Args:
    #         days_from_now: через сколько дней вылет (по умолчанию 7)
    #         trip_days: продолжительность поездки в днях (по умолчанию 7)
    #     """
    #     print(f"Выбираем даты: вылет через {days_from_now} дней, поездка на {trip_days} дней")
        
    #     # Рассчитываем даты
    #     start_date = datetime.now() + timedelta(days=days_from_now)
    #     end_date = start_date + timedelta(days=trip_days)

    #     # Форматируем даты для отображения
    #     start_date_str = start_date.strftime("%d %b")  # Например: "15 мар"
    #     end_date_str = end_date.strftime("%d %b")
        
    #     print(f"Дата вылета: {start_date_str}, Дата возвращения: {end_date_str}")
        
    #     # Кликаем на поле даты вылета, чтобы открыть календарь
    #     date_start_field = self.wait.until(
    #         EC.element_to_be_clickable(self.DATE_START)
    #     )
    #     date_start_field.click()
    #     time.sleep(1)
        
    #     # Выбираем дату вылета
    #     self._select_date_in_calendar(start_date)
        
    #     # Выбираем дату возвращения
    #     self._select_date_in_calendar(end_date)

    # def _enter_date_manually(self, target_date):
    #     """Запасной метод - ввод даты вручную."""
    #     date_str = target_date.strftime("%d.%m.%Y")
        
    #     # Пробуем ввести в поле даты вылета
    #     try:
    #         date_field = self.driver.find_element(*self.DATE_START)
    #         date_field.clear()
    #         date_field.send_keys(date_str)
    #         date_field.send_keys(Keys.RETURN)
    #     except:
    #         pass

    # def click_search(self):
    #     """Нажать кнопку поиска билетов."""
    #     print("Нажимаем кнопку поиска...")
        
    #     search_btn = self.wait.until(
    #         EC.element_to_be_clickable(self.SEARCH_BUTTON)
    #     )
        
    #     # Пробуем обычный клик
    #     try:
    #         search_btn.click()
    #     except:
    #         # Если не получается, кликаем через JavaScript
    #         self.driver.execute_script("arguments[0].click();", search_btn)