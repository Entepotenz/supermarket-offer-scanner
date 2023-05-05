from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class ActionProspectusPdfScraper:
    def __init__(self, headless: bool = False):
        self.main_url = "https://www.lidl.de/c/online-prospekte/s10005610"
        self.options = FirefoxOptions()
        if headless is True:
            self.options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=self.options)

    def __del__(self):
        self.driver.close()

    def get_urls(self) -> [str]:
        self.driver.get(self.main_url)

        cookie_banner = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        cookie_banner.click()

        pdf_downloads = self.driver.find_elements(
            By.XPATH,
            '//*[@id="flyer-overview__content"]//a[@aria-label="Download"]',
        )

        return [item.get_attribute("href") for item in pdf_downloads]
