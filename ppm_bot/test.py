import logging

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

from ppm_bot.config_loader import load_config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

config = load_config()

options = Options()
service = Service(GeckoDriverManager().install())
options.headless = True
driver = Firefox(options=options, service=service)
driver.get("https://google.com")
print(driver.title)
driver.quit()
