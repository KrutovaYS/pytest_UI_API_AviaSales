import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os

@pytest.fixture(scope="function")
def driver():
    """
    Фикстура для запуска браузера перед каждым тестом.
    """
    options = Options()
    # Опция, чтобы браузер не закрывался сразу после ошибки (удобно для отладки)
    # options.add_experimental_option("detach", True)
    
    # Автоматически скачает нужный драйвер и запустит браузер
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)  # Ждем появления элементов до 10 секунд

    yield driver  # Передаем драйвер в тест

    driver.quit()

@pytest.fixture
def PHONE_NUMBER():
    """ Фикстура для получения номера телефона из .env"""
    phone = os.getenv("PHONE_NUMBER")
    if not phone:
        raise ValueError("❌ PHONE_NUMBER не найден в .env файле!")
    return phone