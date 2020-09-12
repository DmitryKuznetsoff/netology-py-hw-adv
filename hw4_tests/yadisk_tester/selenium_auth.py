import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

URL = 'https://passport.yandex.ru/auth/'


class YandexAuth:

    def __init__(self, login, password):
        self.login = login
        self.password = password
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver.get(URL)

    def input_login(self):
        elem = self.driver.find_element_by_name('login')
        elem.send_keys(self.login)
        elem.send_keys(Keys.ENTER)
        time.sleep(1)
        return self.driver.current_url

    def input_password(self):
        elem = self.driver.find_element_by_name('passwd')
        elem.send_keys(self.password)
        elem.send_keys(Keys.ENTER)
        time.sleep(1)
        return self.driver.current_url

    def close_browser(self):
        self.driver.close()
        self.driver.quit()


if __name__ == '__main__':
    login = ''
    pwd = ''
    user = YandexAuth(login, pwd)
    user.input_login()
    user.input_password()
    user.close_browser()
