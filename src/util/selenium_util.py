from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from util.config import Config

class SeleniumUtil:

    @staticmethod
    def get_driver():
        chrome_options = Options()

        # keep the browser open
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--start-maximized")
            
        # ignore insecure certs alert
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['acceptInsecureCerts'] = True

        # get a driver
        driver_path = SeleniumUtil.get_driver_path()
        driver = webdriver.Chrome(
            executable_path=driver_path,
            desired_capabilities=capabilities,
            options=chrome_options
        )
        return driver

    @staticmethod
    def get_driver_path():
        config_file = Config.get_config_file()

        driver_path = config_file["selenium_driver_path"]
        return driver_path

    @staticmethod
    def execute_element_action(self, elements):
        for target in elements.values():
            element = self._web_driver_wait.until(EC.presence_of_element_located((target['by'],target['element'])))

            if (target['action']['type'] == 'key'):
                element.send_keys(target['action']['send_text'])

            if (target['action']['type'] == 'click'):
                element.click()
