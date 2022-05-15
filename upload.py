from selenium import webdriver, common
import json
import os
from urllib.error import HTTPError, URLError
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pydub
import speech_recognition as sr
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.edge.options import Options
import urllib.request

# Define path of html elements
GET_STARTED = "/html/body/div[1]/div/div[2]/div/div/div/button"
IMPORT_WALLET = "/html/body/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/button"
NO_THANKS = "/html/body/div[1]/div/div[2]/div/div/div/div[5]/div[1]/footer/button[1]"
SECRET = "/html/body/div[1]/div/div[2]/div/div/form/div[4]/div[1]/div/input"
NEW_PASS = "/html/body/div[1]/div/div[2]/div/div/form/div[5]/div/input"
NEW_PASS_2 = "/html/body/div[1]/div/div[2]/div/div/form/div[6]/div/input"
ACCEPT = "/html/body/div[1]/div/div[2]/div/div/form/div[7]/div"
GET = "/html/body/div[1]/div/div[2]/div/div/form/button"
ALL_DONE = "/html/body/div[1]/div/div[2]/div/div/button"
WALLET = "//i[text()='account_balance_wallet']/ancestor::button"
METAMASK = "//span[text()='MetaMask']/ancestor::div[1]/ancestor::button"
NEXT = "/html/body/div[1]/div/div[2]/div/div[2]/div[4]/div[2]/button[2]"
CONNECT = "/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/footer/button[2]"
FIRST_SIGN = "/html/body/div[1]/div/div[2]/div/div[3]/button[2]"
PHOTO_INPUT = "/html/body/div[1]/div[1]/main/div/div/section/div[2]/form/div[1]/div/div[2]/input"
NAME_INPUT = "/html/body/div[1]/div[1]/main/div/div/section/div[2]/form/div[2]/div/div[2]/div[1]/input"
DESCRIPTION_INPUT = "/html/body/div[1]/div[1]/main/div/div/section/div[2]/form/div[4]/div/textarea"
PROPERTIES_ADD = "/html/body/div[1]/div[1]/main/div/div/section/div[2]/form/section/div[1]/div/div[2]/button"
SAVE = '//button[text()="Save"]'
POLYGON = "/html/body/div[1]/div[1]/main/div/div/section/div[2]/form/div[7]/div/div[3]/div/div/div/ul/li/button"
ETH = "/html/body/div[1]/div[1]/main/div/div/section/div[2]/form/div[7]/div/div[2]"
CREATE = "/html/body/div[1]/div[1]/main/div/div/section/div[2]/form/div[9]/div[1]/span/button"
BEFORE_X = "//i[@aria-label='Close']/parent::button"
X_BUTTON = "/html/body/div[5]/div/div/div/div[2]/button"
SELL = "/html/body/div[1]/div[1]/main/div/div/div[1]/div/span[2]/a"
INPUT_AMOUNT_POLY = '//input[@name="price"]'
DURATION = "//button[@id='duration']"
INPUT_FOR_DATE = '//input[@value="2022-02-20"]'
FORWARD = "//i[text()='arrow_forward']/ancestor::button"
BACKWARD = "//i[text()='arrow_back']/ancestor::button"
SELECT_DAY = '//button[text()="20"][@class="UnstyledButtonreact__UnstyledButton-sc-ty1bh0-0 Monthreact__Day-sc-rehiga-1 btgkrL cWcHZn"]'
COMPLETE_POLY = "/html/body/div[1]/div[1]/main/div/div/div[3]/div/div[2]/div/div[1]/form/div[5]/button"
POLY_SIGN = '//button[@class="Blockreact__Block-sc-1xf18x6-0 Buttonreact__StyledButton-sc-glfma3-0 kXZare fzwDgL"]'
POLY_SIGN_2 = "/html/body/div[1]/div/div[2]/div/div[3]/button[2]"
WAIT_AFTER_SIGN_POLY = '//h4[text()="Your NFT is listed!"]'
TRYING = '//span[text()="MetaMask"]/ancestor::button'
DESCRIPTION = "They are weird, bizarre, strange and you will love it"
SHARE = '//p[@class="Blockreact__Block-sc-1xf18x6-0 Textreact__Text-sc-1w94ul3-0 gJKZrx cCfKUE AssetSuccessModalContent--share-text"]'
ETH_CLICK_AFTER_COMPLETE = '//div[@class="signature-request-message__scroll-button"]'
ETH_LAST_BUTTON = '//button[@class="button btn--rounded btn-primary btn--large"]'
SECOND_7_DAYS = '//input[@placeholder="Select a date range"]/parent::div'
SIX_MONTHS_BUTTON = '//span[text()="6 months"]/ancestor::button'


class MyError(Exception):
    pass


class Upload:
    def __init__(self):

        self.image_folder_name = "Your image folder name"
        self.metadata_folder_name = "Your meta data folder name"
        self.collection_url = "Your collection url"
        self.secret_phrase = "Your metamask secret phrase"
        self.metamask_password = "Your metamask password"
        self.price = "Price"
        # Starts from this number to upload
        self.start_number = 0
        # This is your folder number, Your project folder should contain a folder named this number
        self.dictionary_number = 1
        self.delay = 10
        self.is_created = False
        self.is_open_create_page = False

        self.run_metamask()
        with open(self.metadata_folder_name) as file:
            self.data = json.load(file)

    # This is used for waiting process
    def wait(self, driver, delay, path, click=False, less_two_elements=False,
             iframe=False):
        try:
            if iframe:
                WebDriverWait(driver, delay).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, path)))
            else:
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, path)))

        except (common.exceptions.TimeoutException, common.exceptions.WebDriverException):

            driver.refresh()
            raise MyError
        else:
            if click:
                if less_two_elements:
                    driver.find_elements(By.XPATH, path)[0].click()
                else:
                    driver.find_element(By.XPATH, path).click()

    # This is used for logging in opensea
    def login_to_opensea(self, driver):

        driver.get("https://opensea.io/")

        self.wait(driver, self.delay, WALLET, click=True)

        self.wait(driver, self.delay, METAMASK)
        element = driver.find_element(By.XPATH, METAMASK)
        driver.execute_script("arguments[0].click();", element)

        WebDriverWait(driver, self.delay).until(EC.number_of_windows_to_be(2))
        driver.switch_to.window(driver.window_handles[1])

        self.wait(driver, self.delay, NEXT, click=True)

        self.wait(driver, self.delay, CONNECT, click=True)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    # This is used for logging in metamask, after login it will call upload function
    def run_metamask(self):
        extension_path = "edge.crx"
        opt = Options()

        opt.add_extension(extension_path)
        opt.page_load_strategy = 'eager'
        opt.add_experimental_option("excludeSwitches", ["enable-automation"])
        opt.add_experimental_option('useAutomationExtension', False)
        opt.add_argument("--start-maximized")
        opt.add_argument("--disable-gpu")
        opt.add_experimental_option("detach", True)

        driver = webdriver.Edge(options=opt)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        self.wait(driver, self.delay, GET_STARTED, click=True)

        self.wait(driver, self.delay, IMPORT_WALLET, click=True)

        self.wait(driver, self.delay, NO_THANKS, click=True)

        self.wait(driver, self.delay, SECRET)
        driver.find_element(By.XPATH, SECRET).send_keys(self.secret_phrase)

        driver.find_element(By.XPATH, NEW_PASS).send_keys(self.metamask_password)

        driver.find_element(By.XPATH, NEW_PASS_2).send_keys(self.metamask_password)

        driver.find_element(By.XPATH, ACCEPT).click()
        driver.find_element(By.XPATH, GET).click()

        self.wait(driver, self.delay, ALL_DONE, click=True)

        try:
            self.login_to_opensea(driver)
        except:
            self.login_to_opensea(driver)

        self.first_create(driver)
        self.upload(driver, self.start_number, self.dictionary_number)

    # This is used for adding properties to the NFT
    def add_properties(self, driver, n):
        number_2 = 0
        # You should change between ### and ### according to your metadata file
        ###
        for i in self.data[n]:
            if i != "tokenId":
                character = i
                prop_name = self.data[n][i]
            else:
                break
            ###

            if number_2 == 0:
                driver.find_element(By.XPATH,
                                    '//input[@placeholder="Character"]').send_keys(character)
                driver.find_element(By.XPATH,
                                    '//input[@placeholder="Male"]').send_keys(prop_name)
                number_2 += 1
                continue
            driver.find_element(By.XPATH,
                                '//button[text()="Add more"]').click()
            try:
                driver.find_element(By.XPATH,
                                    f"/html/body/div[2]/div/div/div/section/table/tbody/tr[{number_2 + 1}]/td[1]/div/div/input").send_keys(
                    character)
                driver.find_element(By.XPATH,
                                    f"/html/body/div[2]/div/div/div/section/table/tbody/tr[{number_2 + 1}]/td[2]/div/div/input").send_keys(
                    prop_name)
            except common.exceptions.NoSuchElementException:
                driver.find_element(By.XPATH,
                                    f"/html/body/div[5]/div/div/div/section/table/tbody/tr[{number_2 + 1}]/td[1]/div/div/input").send_keys(
                    character)
                driver.find_element(By.XPATH,
                                    f"/html/body/div[5]/div/div/div/section/table/tbody/tr[{number_2 + 1}]/td[2]/div/div/input").send_keys(
                    prop_name)
            number_2 += 1

    # This is used for solving the captcha audio file
    def solve_audio(self, driver, dictionary_num):
        try:
            self.wait(driver, 5, '//audio[@id="audio-source"]')
            src = driver.find_element(By.XPATH, '//audio[@id="audio-source"]').get_attribute("src")
            path_to_mp3 = os.path.normpath(
                os.path.join(os.getcwd() + f"\\{dictionary_num}", "sample.mp3"))
            path_to_wav = os.path.normpath(
                os.path.join(os.getcwd() + f"\\{dictionary_num}", "sample.wav"))

            urllib.request.urlretrieve(src, path_to_mp3)

            sound = pydub.AudioSegment.from_mp3(os.getcwd() + f"\\{dictionary_num}\\sample.mp3")

            sound.export(path_to_wav, format="wav")
            sample_audio = sr.AudioFile(os.getcwd() + f"\\{dictionary_num}\\sample.wav")
            r = sr.Recognizer()
            with sample_audio as source:
                audio = r.record(source)
                key = r.recognize_google(audio)

            driver.find_element(By.ID,
                                "audio-response").send_keys(key.lower())
            driver.find_element(By.ID,
                                "audio-response").send_keys(Keys.ENTER)

            time.sleep(0.2)
            error = driver.find_elements(By.XPATH, "//div[@class='rc-audiochallenge-error-message']")

            if len(error) == 1:
                if len(error[0].text) > 10:
                    raise sr.UnknownValueError
        except (sr.UnknownValueError, HTTPError, URLError):
            driver.find_element(By.XPATH, '//button[@class="rc-button goog-inline-block rc-button-reload"]').click()
            self.solve_audio(driver, dictionary_num)

    # This is used for captcha screen
    def solve_recaptcha(self, driver, dictionary_num):
        self.wait(driver=driver, delay=self.delay, path='//iframe[@title="reCAPTCHA"]', iframe=True)
        self.wait(driver, 5, '//div[@class="recaptcha-checkbox-border"]', click=True)  # , frame=True
        driver.switch_to.default_content()
        self.wait(driver, 5, '//iframe[@title="recaptcha challenge expires in two minutes"]', iframe=True)
        self.wait(driver, 5, '//button[@id="recaptcha-audio-button"]')  # , frame=True
        ssd = driver.find_element(By.XPATH, '//button[@id="recaptcha-audio-button"]')
        ssd.click()

        self.wait(driver, 5, "//div[@class='rc-audiochallenge-error-message']")
        self.solve_audio(driver=driver, dictionary_num=dictionary_num)
        driver.switch_to.default_content()

    # This function only called once when creating first NFT
    def first_create(self, driver):
        driver.get(f"{self.collection_url}/assets/create")
        self.is_open_create_page = True
        time.sleep(2)
        self.wait(driver, self.delay, TRYING, click=True)
        WebDriverWait(driver, self.delay).until(
            EC.number_of_windows_to_be(2))
        driver.switch_to.window(driver.window_handles[1])
        self.wait(driver, self.delay, FIRST_SIGN, click=True)
        driver.switch_to.window(driver.window_handles[0])
        self.is_created = True

    # This is the main function used in page of NFT creating
    def create(self, driver, n, dictionary_num):
        try:

            if not self.is_open_create_page:
                driver.get(f"{self.collection_url}/assets/create")
                self.is_open_create_page = True
            self.wait(driver, self.delay, PHOTO_INPUT)
            # Upload Image
            driver.find_element(By.XPATH, PHOTO_INPUT).send_keys(
                os.getcwd() + f"/{self.image_folder_name}/{n}.png")
            # Name
            driver.find_element(By.XPATH, NAME_INPUT).send_keys(
                f"{n}")

            # Description
            driver.find_element(By.XPATH,
                                DESCRIPTION_INPUT).send_keys(DESCRIPTION)

            # Add Properties Button
            driver.find_element(By.XPATH, PROPERTIES_ADD).click()

            # Add Properties Function
            self.add_properties(driver, n)

            # Save Properties
            driver.find_element(By.XPATH, SAVE).click()

            # Create Button
            driver.find_element(By.XPATH, CREATE).click()

            self.solve_recaptcha(driver, dictionary_num)
            # Click x Button
            self.wait(driver, 10, BEFORE_X, click=True)
            self.is_open_create_page = False

        except (MyError, common.exceptions.WebDriverException, common.exceptions.ElementClickInterceptedException):
            self.is_open_create_page = False
            if len(driver.find_elements(By.XPATH, f"//h1[@title='{n}']")) == 1:
                n += 1
                return False
            elif len(driver.find_elements(By.XPATH,
                                          '//h1[@class="Blockreact__Block-sc-1xf18x6-0 Textreact__Text-sc-1w94ul3-0 gJKZrx dgOUEe error--title"]')) == 1:
                n += 1

            self.create(driver, n, dictionary_num)

        else:
            return False

    # This function is used to click sell button after creating NFT
    def sell(self, driver):
        try:
            # Click Sell Button
            self.wait(driver, self.delay, SELL, click=True)
        except MyError:
            self.sell(driver)

    # This function is used for page of selling
    def sell_sign(self, driver):
        try:
            # Send Price
            self.wait(driver, self.delay, INPUT_AMOUNT_POLY)
            driver.find_element(By.XPATH,
                                INPUT_AMOUNT_POLY).send_keys(self.price)

            self.wait(driver, self.delay, DURATION, click=True)
            self.wait(driver, self.delay, SECOND_7_DAYS, click=True)
            self.wait(driver, self.delay, SIX_MONTHS_BUTTON, click=True)
            self.wait(driver, self.delay, "//body", click=True)
            # Complete Poly Click

            self.wait(driver, self.delay, POLY_SIGN, click=True)
            self.wait(driver, self.delay, POLY_SIGN, click=True)  # POLY
            # Signing
            try:
                WebDriverWait(driver, self.delay).until(
                    EC.number_of_windows_to_be(2))
                driver.switch_to.window(driver.window_handles[1])
            except common.exceptions.TimeoutException:
                driver.refresh()
                self.sell_sign(driver)

            self.wait(driver, self.delay, POLY_SIGN_2, click=True)  # POLY

            driver.switch_to.window(driver.window_handles[0])

            self.wait(driver, 5, WAIT_AFTER_SIGN_POLY)  # POLY

        except MyError:
            self.sell_sign(driver)

        return True

    # This is the main function of all process
    def upload(self, driver, n, dictionary_num):
        while True:
            is_created = self.create(driver, n, dictionary_num)
            if not is_created:
                n += 1

            self.sell(driver)
            self.sell_sign(driver)

            with open(f"{os.getcwd()}/{dictionary_num}/uploaded.txt", "a") as file:
                file.write(str(n) + "\n")


if __name__ == "__main__":
    user = Upload()

# This used to change time duration for listing in old version of selling page of opensea
"""

        date = datetime.now()
        day = date.day
        year = date.year
        month = date.month
        first_month_name = month_name[month]
        second_month_name = month_name[month + 6]
        
            self.wait(driver, self.delay,
                      f'//h6[text()="{first_month_name} {year}"]/ancestor::div[1]/descendant::button[text()="{day + 1}"]',
                      click=True,
                      less_two_elements=True)

            self.wait(driver, self.delay,
                      f'//h6[text()="{first_month_name} {year}"]/ancestor::div[1]/descendant::button[text()="{day + 2}"]',
                      click=True,
                      less_two_elements=True)

            self.wait(driver, self.delay,
                      f'//h6[text()="{first_month_name} {year}"]/ancestor::div[1]/descendant::button[text()="{day}"]',
                      click=True,
                      less_two_elements=True)

            if len(driver.find_elements(By.XPATH, BACKWARD)) > 0:
                self.wait(driver, self.delay, BACKWARD, click=True)

            for _ in range(3):
                self.wait(driver, self.delay, FORWARD, click=True)

            self.wait(driver, self.delay,
                      f'//h6[text()="{second_month_name} {year}"]/ancestor::div[1]/descendant::button[text()="{day}"]',
                      click=True,
                      less_two_elements=True)
                      """
