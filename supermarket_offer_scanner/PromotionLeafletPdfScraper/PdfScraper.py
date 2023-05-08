from abc import abstractmethod

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class PdfScraper:
    def __init__(self, headless: bool):
        self.options = FirefoxOptions()
        if headless is True:
            self.options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=self.options)

    def __del__(self):
        self.driver.close()

    @abstractmethod
    def get_urls(self) -> [str]:
        pass

    @staticmethod
    def get_pdf_scraper(shop_name: str, headless: bool = False):
        match shop_name.lower():
            case "aldinord":
                from supermarket_offer_scanner.PromotionLeafletPdfScraper.AldiNordPdfScraper import (
                    AldiNordPdfScraper,
                )

                return AldiNordPdfScraper(headless=headless)
            case "lidl":
                from supermarket_offer_scanner.PromotionLeafletPdfScraper.LidlPdfScraper import (
                    LidlPdfScraper,
                )

                return LidlPdfScraper(headless=headless)
