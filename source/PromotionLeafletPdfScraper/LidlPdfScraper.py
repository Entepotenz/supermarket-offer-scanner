from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from .PdfScraper import PdfScraper


class LidlPdfScraper(PdfScraper):
    main_url = "https://www.lidl.de/c/online-prospekte/s10005610"

    def __init__(self, headless: bool):
        PdfScraper.__init__(self, headless=headless)

    def get_urls(self) -> [str]:
        self.driver.get(self.main_url)

        cookie_banner = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.ID, "onetrust-accept-btn-handler")
            )
        )
        cookie_banner.click()

        pdf_downloads = self.driver.find_elements(
            By.XPATH,
            '(//*[@id="flyer-overview__content"]//a[@aria-label="Download"])[2]',
        )

        return [item.get_attribute("href") for item in pdf_downloads]
