from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from .PdfScraper import PdfScraper


class HitPdfScraper(PdfScraper):
    main_url = "https://www.hit.de/handzettel-muenster/aktuell.html"

    def __init__(self, headless: bool):
        PdfScraper.__init__(self, headless=headless)

    def get_urls(self) -> list[str]:
        self.driver.get(self.main_url)

        cookie_banner = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(), "Nur Notwendige erlauben")]')
            )
        )
        cookie_banner.click()

        pdf_downloads = self.driver.find_elements(
            By.XPATH,
            '//span[contains(text(), "Download")]/parent::a',
        )

        hrefs: list[str] = []
        for item in pdf_downloads:
            href = item.get_attribute("href")
            if href is not None:
                hrefs.append(href)

        return hrefs
