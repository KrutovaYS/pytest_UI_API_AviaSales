import re
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.mainPage import MainPage


class ResultPage:
    """Класс для работы со страницей результатов поиска."""
    # Локаторы
    RESULTS_LIST = (By.XPATH, '//div[@data-test-id="search-results-items-list"]')
    FIRST_TICKET_PRICE = (By.XPATH, '(//div[@data-test-id="price"])[1]')
    ANY_TICKET_PRICE = (By.XPATH, '//div[@data-test-id="price"]')
    # Сообщение об отсутствии билетов (варианты текста на Aviasales)
    NO_RESULTS_MESSAGE = (By.XPATH, '//*[contains(., "Ничего не найдено") or contains(., "Ничего не нашлось")]')
    FAVORITE_BUTTON = (By.XPATH, "//button[@data-test-id='button']")
    LOGIN_FORM = (By.XPATH, "//div[@data-test-id='login-form']")
    LOGIN_FORM_TITLE = (
        By.XPATH,
        "//div[@role='dialog' and @aria-modal='true']"
        "//h2[@data-test-id='text' and contains(normalize-space(.), 'Войдите в')]"
    )

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def wait_for_results_ready(self, timeout: int = 45) -> None:
        """Дождаться загрузки страницы результатов (список или хотя бы одна цена в DOM)."""
        self.wait.until(   # WebDriverWait(self.driver, timeout)
            EC.presence_of_element_located(self.ANY_TICKET_PRICE)
        )

    def get_first_price(self) -> str:
        """Получить цену первого билета"""
        price_element = self.wait.until(
            EC.visibility_of_element_located(self.FIRST_TICKET_PRICE)
        )
        return price_element.text.strip()
        #  Или так, если тест упал
        #  price_element = self.wait.until(
        # EC.visibility_of_element_located(self.FIRST_TICKET_PRICE)
        # )
        # self.wait.until(EC.visibility_of(price_element))
        # return price_element.text.strip()

    def is_price_valid(self, price_text: str) -> bool:
        """Проверка, что строка похожа на цену (содержит цифры)."""
        if not price_text:
            return False
        return bool(re.search(r'\d', price_text))

    def has_results(self) -> bool:
        """Проверка, что на странице есть хотя бы один результат (цена)."""
        try:
            short_wait = WebDriverWait(self.driver, 5)
            short_wait.until(
                EC.visibility_of_element_located(self.ANY_TICKET_PRICE)
            )
            return True
        except Exception:
            return False

    def has_no_results(self, timeout: int = 20) -> bool:
        """
        Проверка сценария «нет билетов»: отображается сообщение об отсутствии результатов
        или нет ни одной видимой цены (страница результатов уже загрузилась).
        """
        short_wait = WebDriverWait(self.driver, timeout)
        # Вариант 1: видно сообщение «ничего не найдено» / «нет рейсов»
        try:
            msg = short_wait.until(
                EC.visibility_of_element_located(self.NO_RESULTS_MESSAGE)
            )
            if msg and msg.is_displayed():
                return True
        except Exception:
            pass
        # Вариант 2: блок результатов есть, но видимых цен нет (пустой список)
        try:
            list_el = self.driver.find_element(*self.RESULTS_LIST)
            if list_el.is_displayed():
                prices = self.driver.find_elements(*self.ANY_TICKET_PRICE)
                visible_prices = [p for p in prices if p.is_displayed()]
                if len(visible_prices) == 0:
                    return True
        except Exception:
            pass
        return False
    
    def click_favourite_button(self):
        # Нажимаем на сердечко у первого билета
        btn_heart = self.wait.until(
                EC.element_to_be_clickable(self.FAVORITE_BUTTON)
            )
        btn_heart.click()

    def is_login_form_displayed(self) -> bool:
        """Проверить, отображается ли форма входа"""
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.LOGIN_FORM_TITLE)
            ).is_displayed()
        except:
            return False
        
    def get_login_form_text(self) -> str:
        """Получить текст формы входа"""
        try:
            return self.driver.find_element(*self.LOGIN_FORM_TITLE).text
        except:
            return ""
    
    def add_to_favourite_without_auth(self):
        """Попытка добавить в избранное без авторизации"""
        main_page = MainPage(self.driver)
        main_page.open()
        # Шаг 2. Вводим поисковые параметры: город Откуда, город Куда, дата вылета, дата прибытия
        main_page.enter_origin('Владивосток')
        main_page.enter_destination('Самара')
        main_page.enter_date_start('19.03.2026')
        main_page.enter_date_end('20.03.2026')

        # Шаг 3. Нажимаем кнопку Найти билеты
        main_page.enter_search_btn()
        self.click_favourite_button()
        assert self.is_login_form_displayed(), "Форма входа не появилась"
        return self.get_login_form_text()
    
    


               
        
        