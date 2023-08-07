from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
import os
import time

class DataScrapper:
    def __init__(self) -> None:
        self.__download_path = os.path.abspath(r'.\media\gameplay')
        # SELENIUM
        self.__options = Options()
        self.__options.headless = True
        self.__options.set_preference(
            'browser.download.dir', self.__download_path)
        self.__options.set_preference("browser.download.folderList", 2)
        self.__options.add_argument('--log-level=3')
        self.driver = None
        self.initialize_driver()

    def initialize_driver(self):
        retries = 3  # Number of retries
        for attempt in range(retries):
            try:
                gecko_driver_path = GeckoDriverManager().install()
                self.driver = webdriver.Firefox(service=FirefoxService(gecko_driver_path), options=self.__options)
                self.driver.maximize_window()
                break  # Successfully initialized the driver
            except Exception as e:
                print(f"Error initializing driver: {e}")
                if attempt < retries - 1:
                    print(f"Retrying in 10 seconds...")
                    time.sleep(10)  # Wait for 10 seconds before retrying
                else:
                    raise  # Raise the exception after all retries

    def quit(self):
        if self.driver:
            self.driver.quit()

# # Example usage:
# try:
#     scrapper = DataScrapper()
#     # Use scrapper.driver for scraping
# finally:
#     scrapper.quit()
