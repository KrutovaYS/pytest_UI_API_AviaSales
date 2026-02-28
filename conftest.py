import pytest
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from dotenv import load_dotenv
import os


@pytest.fixture(scope="function")
def driver() -> WebDriver:
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

    # Проверить перед закрытием
    if driver:
        driver.quit()

        
# Отказаться от авторизации, не подставляется токен
# load_dotenv()

# @pytest.fixture
# def _guestia_key():
#     """Фикстура для получения _guestia_key из .env"""
#     key = os.getenv('_GUESTIA_KEY')
#     if not key:
#         pytest.skip("Ключ _guestia_key не найден в .env файле")
#     return key

# @pytest.fixture
# def driver_with_auth(driver: WebDriver, _guestia_key):
#     """Фикстура для драйвера с авторизацией"""
#     driver.get("https://www.aviasales.ru/")
    
#     # Сначала удаляем старую куку, если есть
#     try:
#         driver.delete_all_cookie()
#     except:
#         pass
    
#     # 3. Добавляем куку с правильными параметрами
#     driver.add_cookie({
#         "name": "_guestia_key",
#         "value": _guestia_key,
#         "domain": ".aviasales.ru",
#         "path": "/",
#         "secure": True,
#         "httpOnly": True
#     })
    
#     # 4. Обновляем страницу
#     driver.refresh()
           
#     return driver