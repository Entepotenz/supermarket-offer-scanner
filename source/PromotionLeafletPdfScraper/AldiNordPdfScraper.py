import time

from selenium.webdriver.common.by import By

from .PdfScraper import PdfScraper


class AldiNordPdfScraper(PdfScraper):
    main_url = "https://www.aldi-nord.de/prospekte/aldi-vorschau.html"

    def __init__(self, headless: bool):
        PdfScraper.__init__(self, headless=headless)

    def get_urls(self) -> list[str]:
        self.driver.get(self.main_url)

        time.sleep(10)
        cookie_banner = self.driver.execute_script(
            """return document.querySelector('div#usercentrics-root').shadowRoot.querySelector('button[data-testid="uc-deny-all-button"]')"""
        )
        cookie_banner.click()

        pdf_downloads = self.driver.find_elements(
            By.XPATH,
            '//a[contains(text(), "Download")]',
        )

        return [item.get_attribute("href") for item in pdf_downloads]
