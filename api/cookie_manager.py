import requests
import json
import os
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class CookieManager:
    def __init__(self, cookie_file="aviasales_cookies.json"):
        self.cookie_file = cookie_file
        
    def get_fresh_cookies(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--window-size=1920,1080')
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        try:
            driver.get("https://www.aviasales.ru")
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            cookies = {}
            for cookie in driver.get_cookies():
                cookies[cookie['name']] = cookie['value']
            return cookies
        finally:
            driver.quit()
    
    def save_cookies(self, cookies):
        data = {
            'cookies': cookies,
            'expires': (datetime.now() + timedelta(minutes=30)).isoformat()
        }
        with open(self.cookie_file, 'w') as f:
            json.dump(data, f)
    
    def load_cookies(self):
        if not os.path.exists(self.cookie_file):
            return None
        with open(self.cookie_file, 'r') as f:
            data = json.load(f)
        expires = datetime.fromisoformat(data['expires'])
        if datetime.now() < expires:
            return data['cookies']
        return None
    
    def get_valid_cookies(self):
        cookies = self.load_cookies()
        if cookies:
            return cookies
        cookies = self.get_fresh_cookies()
        self.save_cookies(cookies)
        return cookies
    
    def format_cookie_header(self, cookies):
        cookie_parts = []
        for name, value in cookies.items():
            cookie_parts.append(f"{name}={value}")
        return '; '.join(cookie_parts)
    
    def request(self, method, url, **kwargs):
        cookies = self.get_valid_cookies()
        
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'origin': 'https://www.aviasales.ru',
            'referer': 'https://www.aviasales.ru/',
            'Cookie': self.format_cookie_header(cookies)
        }
        
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
        kwargs['headers'] = headers
        kwargs['cookies'] = cookies
        
        return requests.request(method, url, **kwargs)
