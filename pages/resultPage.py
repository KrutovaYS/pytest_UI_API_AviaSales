from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class ResultPage:
    """ Класс для работы со страницей результатов поиска """
    # Локаторы
    RESULTS_LIST = (By.XPATH, '//div[@data-test-id="search-results-items-list"]')  # окно с результатами
    FIRST_TICKET_PRICE = (By.XPATH, '(//div[@data-test-id="price"])[1]')  # Локатор цены первого билета
    ANY_TICKET_PRICE = (By.XPATH, '//div[@data-test-id="price"]')  # Локатор находит все элементы с ценами

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 60)

    def get_first_price(self) -> str:
        """Получить цену первого билета"""
        price_element = self.wait.until(
            EC.presence_of_element_located(self.FIRST_TICKET_PRICE)
        )
        return price_element.text
    


    # видимо долгое ожидание результата, отказаться от этой проверки
    # def wait_for_results(self):
    #     """Ожидание появления результатов поиска"""
    #     return self.wait.until(
    #         EC.presence_of_element_located(self.RESULTS_LIST)
    #     )

    # def is_results_displayed(self) -> bool:
    #     """Проверка, что результаты поиска отобразились"""
    #     try:
    #         return self.wait_for_results().is_displayed()
    #     except:
    #         return False

    