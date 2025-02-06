from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()


"""
YOUTUBE SIGNIN
aria-label="Sign in"
Youtube Sign in button with the aria-label sign in has an href that redirects to accounts.google.com
"""

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")


def save_netscape_cookies(cookies, filename):
    with open(filename, "w") as f:
        for cookie in cookies:
            domain = cookie["domain"].lstrip(".")
            domain_flag = "TRUE" if cookie["domain"].startswith(".") else "FALSE"
            path = cookie["path"]
            secure = "TRUE" if cookie["secure"] else "FALSE"
            expiry = str(int(cookie.get("expiry", 0)))
            name = cookie["name"]
            value = cookie["value"]

            line = f"{domain}\t{domain_flag}\t{path}\t{secure}\t{expiry}\t{name}\t{value}\n"
            f.write(line)


def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://www.youtube.com")

        sign_in_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[aria-label*="Sign in"]'))
        )
        sign_in_button.click()

        WebDriverWait(driver, 15).until(EC.url_contains("accounts.google.com"))

        email_field = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, "identifierId"))
        )
        email_field.send_keys(EMAIL)

        driver.find_element(By.ID, "identifierNext").click()

        password_field = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.NAME, "Passwd"))
        )
        password_field.send_keys(PASSWORD)

        driver.find_element(By.ID, "passwordNext").click()

        WebDriverWait(driver, 30).until(EC.url_contains("youtube.com"))

        cookies = driver.get_cookies()

        save_netscape_cookies(cookies, "youtube_cookies.txt")

        print("Cookies saved successfully!")

    finally:
        # Close browser quickly
        driver.quit()


if __name__ == "__main__":
    main()
