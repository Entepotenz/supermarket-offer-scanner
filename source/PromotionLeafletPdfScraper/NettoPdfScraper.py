import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from .PdfScraper import PdfScraper


class NettoPdfScraper(PdfScraper):
    main_url = "https://www.netto-online.de/ueber-netto/Online-Prospekte.chtm"

    def __init__(self, headless: bool):
        PdfScraper.__init__(self, headless=headless)

    def get_urls(self) -> [str]:
        self.driver.get(self.main_url)

        time.sleep(10)
        cookie_banner = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(), "Auswahl erlauben")]')
            )
        )
        cookie_banner.click()

        browse_button = self.driver.find_elements(
            By.XPATH,
            '//span[contains(text(), "Jetzt blättern")]',
        )
        browse_button[0].click()

        pdf_downloads = self.driver.find_elements(
            By.XPATH,
            '//span[contains(text(), "PDF herunterladen")]/parent::a',
        )

        return [item.get_attribute("href") for item in pdf_downloads]
