from abc import abstractmethod

from selenium import webdriver


class PdfScraper:
    def __init__(self, headless: bool):
        self.options = webdriver.ChromeOptions()
        if headless is True:
            self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--disable-dev-shm-usage")  # Not used
        self.driver = webdriver.Chrome(options=self.options)

    def __del__(self):
        self.driver.close()

    @abstractmethod
    def get_urls(self) -> [str]:
        pass

    @staticmethod
    def get_pdf_scraper(shop_name: str, headless: bool = False):
        match shop_name.lower():
            case "aldinord":
                from .AldiNordPdfScraper import (
                    AldiNordPdfScraper,
                )

                return AldiNordPdfScraper(headless=headless)
            case "lidl":
                from .LidlPdfScraper import (
                    LidlPdfScraper,
                )

                return LidlPdfScraper(headless=headless)
