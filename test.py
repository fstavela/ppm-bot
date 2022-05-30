from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager


options = Options()
service = Service(GeckoDriverManager().install())
options.headless = True
driver = Firefox(options=options, service=service)
driver.get("https://google.com")
print(driver.title)
driver.quit()
