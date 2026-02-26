import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class AuthPage:

    def __init__(self, __driver: WebDriver) ->None:
        self.__driver = __driver

    # Нажать Войти
    def click_enter(self):
        btn_enter = self.__driver.find_element(By.XPATH, "//button[contains(text(), 'Войти')]")
        btn_enter.click()

    # Нажать на Еще 4 способа
    def choice_of_method(self):
        btn_choice = self.__driver.find_element(By.XPATH, "//button[contains(text(), 'Ещё 4 способа')]")
        btn_choice.click()

    # Ввести номер телефона
    def enter_phone_number(self, phone_number):
        # 1. Нажимаем на поле ввода номера телефона
        input_field = self.__driver.find_element(By.CSS_SELECTOR, "[data-test-id='method-button-phone-number']")
        input_field.click()
        # 2. вводим номер телефона
        input_phone = self.__driver.find_element(By.ID, "phone-input")
        input_phone.send_keys(phone_number)

    