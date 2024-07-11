import scrapy
from scrapy_selenium import SeleniumRequest
from ..items import AmazonItem
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.remote_connection import LOGGER as seleniumLogger
from selenium.common.exceptions import TimeoutException
import logging

seleniumLogger.setLevel(logging.WARNING)
logging.getLogger('scrapy').setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

class AmazonOfertasSpider(scrapy.Spider):
    name = "amazon_ofertas"
    allowed_domains = ["amazon.com"]
    start_urls = ["https://www.amazon.com/-/es/gp/goldbox"]

    def __init__(self, limit, *args, **kwargs):
        super(AmazonOfertasSpider).__init__(*args, **kwargs)
        self.limit = int(limit)

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        driver = response.meta['driver']
        driver.implicitly_wait(5)
        wait = WebDriverWait(driver, 5, 3)

        pos = 1
        for i in range(self.limit):
            # GET CARD
            card = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[@data-testid='product-card' and @data-csa-c-posx='{pos}']")))

            # GET DATA
            product = AmazonItem()
            product['name'] = card.find_element(By.CLASS_NAME, "a-truncate-full").get_attribute('textContent')
            product['discount'] = card.find_element(By.CSS_SELECTOR, ".a-size-mini + span").get_attribute("innerHTML")
            product['link'] = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            product['img'] = card.find_element(By.CSS_SELECTOR, "img").get_attribute('src')
            yield product

            # GET NEXT CARD
            pos += 1
            try:
                card = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[@data-testid='product-card' and @data-csa-c-posx='{pos}']")))
            except TimeoutException:
                try:
                    btnNext = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@data-testid='load-more-view-more-button']")))
                    btnNext.click()
                    card = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[@data-testid='product-card' and @data-csa-c-posx='{pos}']")))
                except TimeoutException:
                    pos += 1
                    card = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[@data-testid='product-card' and @data-csa-c-posx='{pos}']")))

            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth',block: 'center',inline: 'center'});", card)
            
            # # BREAK FROM WHILE LOOP
            # i += 1
            # if i == self.limit:
            #     break