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
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        )
        self.options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=self.options)

    def __del__(self):
        self.driver.close()

    @abstractmethod
    def get_urls(self) -> list[str]:
        pass

    @staticmethod
    def get_pdf_scraper(shop_name: str, headless: bool = False):
        match shop_name.lower():
            case "aldinord":
                from .AldiNordPdfScraper import AldiNordPdfScraper

                return AldiNordPdfScraper(headless=headless)
            case "lidl":
                from .LidlPdfScraper import LidlPdfScraper

                return LidlPdfScraper(headless=headless)
            case "hit":
                from .HitPdfScraper import HitPdfScraper

                return HitPdfScraper(headless=headless)
            case "netto":
                from .NettoPdfScraper import (
                    NettoPdfScraper,
                )

                return NettoPdfScraper(headless=headless)
