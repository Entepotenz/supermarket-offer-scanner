from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from supermarket_offer_scanner.PromotionLeafletPdfScraper.PdfScraper import PdfScraper


class AldiNordPdfScraper(PdfScraper):
    main_url = "https://www.aldi-nord.de/prospekte/aldi-vorschau.html"

    def __init__(self, headless: bool):
        PdfScraper.__init__(self, headless=headless)

    def get_urls(self) -> [str]:
        self.driver.get(self.main_url)

        cookie_banner = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        cookie_banner.click()

        pdf_downloads = self.driver.find_elements(
            By.XPATH,
            '//a[contains(text(), "Download")]',
        )

        return [item.get_attribute("href") for item in pdf_downloads]
