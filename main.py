from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from selenium.webdriver.common.keys import Keys

PROMISED_DOWN = 100
PROMISED_UP = 100
CHROME_DRIVER_PATH = "./ChromeDriver/chromedriver.exe"
TWITTER_EMAIL = "YOUR EMAIL"
TWITTER_PASSWORD = "YOUR PASSWORD"
SPEEDTEST_WEBSITE = "https://www.speedtest.net/"


class InternetSpeedTwitterBot:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        self.driver.get(url=SPEEDTEST_WEBSITE)
        try:
            accept_btn = self.driver.find_element_by_class_name(name="evidon-barrier-acceptbutton")
            accept_btn.click()
        except NoSuchElementException:
            pass

        go_btn = self.driver.find_element_by_class_name(name="js-start-test")
        go_btn.click()

        sleep(60)

        self.down = self.driver.find_element_by_class_name(name="download-speed").text
        print(f"Down : {self.down}")

        self.up = self.driver.find_element_by_class_name(name="upload-speed").text
        print(f"Up : {self.up}")

    def tweet_at_provider(self):
        self.driver.get(url="https://twitter.com/login")
        self.driver.maximize_window()

        sleep(3)

        email = self.driver.find_element_by_name(name="session[username_or_email]")
        email.send_keys(TWITTER_EMAIL)

        password = self.driver.find_element_by_name(name="session[password]")
        password.send_keys(TWITTER_PASSWORD)
        password.send_keys(Keys.ENTER)

        sleep(5)

        text_area = self.driver.find_element_by_class_name(name="public-DraftEditor-content")
        text_area.send_keys(f"""
        Hey Internet Provider, why is my internet speed {self.down}down/{self.up}up 
        when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up.
        """)
        tweet_btn = self.driver.find_element_by_xpath(
            xpath='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/div/span/span')
        tweet_btn.click()


bot = InternetSpeedTwitterBot()
bot.get_internet_speed()
bot.tweet_at_provider()
