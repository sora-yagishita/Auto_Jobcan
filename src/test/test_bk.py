import base64
from operator import contains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from util.selenium_util import SeleniumUtil as su
from selenium.webdriver.support import expected_conditions as EC
from util.config import Config
from util.element import ElementConfig
from util.file_control import FileControl as fctrl
import selenium.common.exceptions as exceptions
import time

class TestCase:

    def __init__(self):
        self._driver = su.get_driver()
        self._web_driver_wait = WebDriverWait(self._driver, Config.get_wait_timeout())
        self.is_manager_test = Config.is_manager_test()
        self.is_open_front_page = Config.is_open_front_page_test()
        self.manager_login_page_elements = ElementConfig.get_login_page_elements()
        self.is_production = Config.get_is_production()
        self.is_login = Config.get_is_login()
        self.is_cart_in = Config.get_is_cart_in()
        self.brands = Config.get_all_brand_top_pages()
        self.ec_manager_menu = Config.get_ec_manager_menu()
        self.login_acount_mail = Config.get_login_acount_mail()
        self.login_acount_pass = Config.get_login_acount_pass()

    def start(self):
        if self.is_open_front_page:
            self.open_front_site()

        if self.is_manager_test:
            self.manager_sign_in()

    def open_front_site(self):
        for brand in self.brands:
            url = brand["top_page"]
            if self.is_production == False:
                url = url.replace('https://', 'https://test.')
            result = self.check_error_page(url, brand)

            if result:
                print(brand["site_name"] + ":OK")
            else:
                print(brand["site_name"] + ":NG")

    def manager_sign_in(self):
        for brand in self.brands:
            menu = brand["manager"]
            for url in menu.values():
                if self.is_production == False:
                    url = url.replace('mgr', 'test')
                result = self.check_error_page(url, brand)

                if result:
                    su.execute_element_action(self, self.manager_login_page_elements)
                    # TODO:ちゃんとログ出力させる
                    print(brand["site_name"] + ":OK")
                else:
                    print(brand["site_name"] + ":NG")

    def check_error_page(self, url, brand):
        try: 
            self._driver.execute_cdp_cmd("Network.enable", {})
            self._driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": self.get_auth_header('w2user', 'vost4er#')})
            self._driver.get(url)
            if self.is_login:
                self.front_site_sign_in(url)
            if self.is_cart_in:
                self.front_site_cart_in_product(url, brand)
            self._web_driver_wait.until(EC.presence_of_element_located((By.TAG_NAME,"meta")))

        except exceptions.TimeoutException:
            print(f"TimeoutException occurs in {url}")
            return False

        page_source = self._driver.page_source
        error_page_patterns = [ r"(?:説明:)[\s\S]*(?:例外の詳細:)[\s\S]*(?:ソース エラー:)", r"(?:<title>)[\s\S]*エラーページ[\s\S]*(?:<\/title>)" ]
        is_error_page = fctrl.find_with_multiple_regex_patterns(page_source, error_page_patterns)
        return (is_error_page == False)

    def front_site_sign_in(self, url):
        if self.is_production:
            self._driver.get(url + "Form/Login.aspx?nurl=%2f")
            #self._driver.find_element_by_xpath('//*[@class="loginBtn"]/ul/li/a').click()
            if(self._driver.current_url != url):
                login_mail_text = self._driver.find_element_by_name("loginAccount")
                login_mail_text.send_keys(self.login_acount_mail)
                login_pass_text = self._driver.find_element_by_name("loginPass")
                login_pass_text.send_keys(self.login_acount_pass)
                self._driver.find_element_by_xpath('//*[@class="member__btn__wrapper"]/button').click()
        else:
            self._driver.get(url + "Form/Login.aspx?nurl=%2f")
            self._driver.find_element_by_xpath('//*[@class="loginBtn"]/ul/li/a').click()
            self._driver.execute_cdp_cmd("Network.enable", {})
            self._driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": self.get_auth_header('chk-macusr', 'm8-G7=Xp')})
            self._driver.get(self._driver.current_url)
            if(contains(self._driver.current_url, "LoginInfoRecv.aspx") == 0):
                login_mail_text = self._driver.find_element_by_name("loginAccount")
                login_mail_text.send_keys(self.login_acount_mail)
                login_pass_text = self._driver.find_element_by_name("password")
                login_pass_text.send_keys(self.login_acount_pass)
                self._driver.find_element_by_xpath('//*[@class="member__btn__wrapper"]/button').click()
                self._driver.execute_cdp_cmd("Network.enable", {})
                self._driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": self.get_auth_header('w2user', 'vost4er#')})
                self._driver.get(self._driver.current_url)
            else:
                self._driver.execute_cdp_cmd("Network.enable", {})
                self._driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": self.get_auth_header('w2user', 'vost4er#')})
                self._driver.get(self._driver.current_url)

            

    def front_site_cart_in_product(self, url, brand):
        self._driver.get(url + "Form/Order/CartList.aspx?ckbn=1&pid1=" + brand["product"] + "&vid1=" + brand["variation"] + "&prdcnt1=1")
        #self._web_driver_wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="btn-next"]')))
        #self._driver.find_element_by_xpath('//*[@class="btn-next"]').click()
        #self._web_driver_wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="btn-next"]')))
        #self._driver.find_element_by_xpath('//*[@class="btn-next"]').click()

    def get_auth_header(self, user, password):
        b64 = "Basic " + base64.b64encode('{}:{}'.format(user, password).encode('utf-8')).decode('utf-8')
        return {"Authorization": b64}