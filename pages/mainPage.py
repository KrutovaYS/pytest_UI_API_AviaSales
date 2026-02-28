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
    ORIGIN_INPUT = (By.XPATH, "//input[@data-test-id='origin-input']")  # Откуда
    DESTINATION_INPUT = (By.XPATH, "//input[@data-test-id='destination-input']")  # Куда
    DATE_START = (By.XPATH, "//button[@data-test-id='start-date-field']")  # Дата вылета
    DATE_CLICK = (By.XPATH, "//button[@aria-label='четверг, 19 марта 2026 г.']")  ## убрать, не использую
    DATE_END = (By.CSS_SELECTOR, "[data-test-id='end-date-value']")  # Дата возвращения/прибытия
    SEARCH_BUTTON = (By.XPATH, "//button[@data-test-id='form-submit']")  # Кнопка поиска

    # Дополнительные локаторы для выпадающих списков
    DATE_CALENDAR = (By.XPATH, "//div[@data-test-id='dropdown']")  # выпадающий календарь для выбора дат вылета/прилета
    DATE_DAY_IN_CALENDAR = (By.XPATH, "//div[@data-test-id='date-19.03.2026']")  # дата вылета в календаре
    ORIGIN_SUGGEST = (By.XPATH, "//ul[@id='avia_form_origin-menu']")  # работает - оставляем 
    DESTINATION_SUGGEST = (By.CSS_SELECTOR, "ul.suggest__list li:first-child")  # Пробуем этот локатор по аналогии с origin, его не нашла

     # Локатор кнопки принятия куки (на основе скриншота)
    # COOKIE_ACCEPT_BUTTON = (By.XPATH, "//button[@data-test-id='accept-cookies-button']")
    COOKIE_ACCEPT_BUTTON = (By.XPATH, "//button[@data-test-id='accept-cookies-button']")

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def open(self) -> None:
        """ Открыть главную страницу"""
        self.driver.get(base_url)
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

        # Проверяем, что баннер куки исчез
        try:
            cookie_banner = self.driver.find_element(*self.COOKIE_ACCEPT_BUTTON)
            return not cookie_banner.is_displayed()
        except:
            return True  # Баннера нет - значит куки приняты

    # Проверяем Куки
    def get_cookie_value(self, cookie_name: str) -> dict:
        """Получить значение куки"""
        return self.driver.get_cookie(cookie_name)
    
    def enter_origin(self, city: str) -> None:
        """ Ввести город вылета в поле Откуда"""
        origin_field = self.wait.until(
            EC.element_to_be_clickable(self.ORIGIN_INPUT)
        )

        # 2. Ждем, пока автоподстановка заполнит поле
        #    Это заменяет time.sleep(1)
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
                print("Выбран первый пункт списка")
            except:
                origin_field.send_keys(Keys.RETURN)
                print("Нажат Enter")

    # Проверка поля Откуда
    def get_origin_value(self) -> str:
        """Получить значение из поля Откуда"""
        origin_field = self.wait.until(
            EC.presence_of_element_located(self.ORIGIN_INPUT)
        )
        return origin_field.get_attribute('value')

    def enter_destination(self, city_destination):
        """Ввести город назначения."""
        dest_city = self.wait.until(
            EC.element_to_be_clickable(self.DESTINATION_INPUT)
        )
        dest_city.clear()
        dest_city.send_keys(city_destination)

        # Диагностика
        time.sleep(2)  # ждем появления списка

        # Ищем все выпадающие списки
        all_lists = self.driver.find_elements(By.TAG_NAME, "ul")
        print(f"\n🔍 Найдено списков: {len(all_lists)}")

        for i, ul in enumerate(all_lists[:10]):  # первые 10
            ul_id = ul.get_attribute('id')
            ul_class = ul.get_attribute('class')
            ul_data_test = ul.get_attribute('data-test-id')
            print(f"  Список {i}: id='{ul_id}', class='{ul_class[:30]}', data-test-id='{ul_data_test}'")

        # Посмотрим первый пункт
        try:
            first_li = ul.find_element(By.TAG_NAME, "li")
            print(f"    Первый пункт: '{first_li.text[:50]}'")
        except:
            pass

        # Пока используем Enter
        dest_city.send_keys(Keys.RETURN)

        # # Ждем появления выпадающего списка
        # self.wait.until(EC.element_to_be_clickable(self.DESTINATION_SUGGEST))  # или visibility_of_element_located

        #  # Выбираем пункт с кодом KUF (Самара)
        # try:
        #     # Ищем элемент с кодом KUF
        #     kuf_locator = (By.XPATH, "//li[contains(text(), 'KUF')]")
        #     kuf_option = self.wait.until(
        #         EC.element_to_be_clickable(kuf_locator)
        #     )
        #     kuf_option.click()
        #     print("Выбран Самара (KUF)")
        # except:
        #     # Если не нашли KUF - первый пункт
        #     try:
        #         first_option = self.driver.find_element(*self.DESTINATION_SUGGEST)
        #         first_option.click()
        #         print("Выбран первый пункт списка")
        #     except:
        #         dest_field.send_keys(Keys.RETURN)
        #         print("Нажат Enter")

        # # Проверка поля Куда
        # #  Получить значение из поля Куда
        # dest_field = self.wait.until(
        #     EC.presence_of_element_located(self.DESTINATION_INPUT)
        # )
        # return dest_field.get_attribute('value')

    def enter_date_start(self, start_date):
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

    """ Проверка поля дата вылета """
    def get_start_date_value(self) -> str:
        """Получить значение даты вылета"""
        date_field = self.wait.until(
            EC.presence_of_element_located(self.DATE_START)
        )
        return date_field.text

    def enter_date_end(self, end_date):
        """ Ввести дату прибытия"""
        date_end = self.wait.until(
            EC.element_to_be_clickable(self.DATE_END)
        )
        date_end.click()
        self.wait.until(EC.visibility_of_element_located(self.DATE_CALENDAR))
        # Ищем родительскую кнопку (более надежно)
        button_locator = (By.XPATH, f"//div[@data-test-id='date-{end_date}']/ancestor::button")
        day_button = self.wait.until(
            EC.element_to_be_clickable(button_locator)
        )
        day_button.click()

    # Проверка поля дата прибытия
    def get_end_date_value(self) -> str:
        """Получить значение даты возвращения"""
        date_field = self.wait.until(
            EC.presence_of_element_located(self.DATE_END)
        )
        return date_field.text

    def enter_search_btn(self):
        """Нажать кнопку поиска билетов."""
        search_btn = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_BUTTON)
        )
        search_btn.click()

        # Добавить новые методы для проверок
    
    
        
    
    
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
    #     