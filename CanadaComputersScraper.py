import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
import time
import requests
import os

MY_ACC = ""
MY_PW = ""


this_url = (
    "https://www.canadacomputers.com/product_info.php?cPath=4_64_1969&item_id=183431"
)


class CanadaComputers:
    """Purchases specified item from https://www.canadacomputers.com/

    Attributes:
        url: url of item
        user: username of canada computers account
        pw: password of canada computers account

    """

    def __init__(self, url, user, pw):
        """Initialize CanadaComputers Object"""
        self.url = url
        self.user = user
        self.pw = pw
        self.driver = webdriver.Chrome()

    def open_browser(self):
        """Maximize browser and open specified url"""
        self.driver.maximize_window()
        self.driver.get(self.url)

    def clickable_id(self, _id):
        """Find clickable element by id"""

        element = WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable((By.ID, _id))
        )

        element.click()

    def clickable_css(self, _css):
        "Find clickable element by css selector"

        element = WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, _css))
        )

        element.click()

    def login(self, tag, username=None, password=None):
        """
        Login into Canada Computers account

        Args:
            tag: input element id
            username: Canada Computers username
            password: Canada Computers password

        Returns:
            input_: username of password
        """

        input_ = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.ID, tag))
        )

        if username != None:
            input_.send_keys(self.user)
        elif password != None:
            input_.send_keys(self.pw)

    def pick_city(self):
        """
        Choose pick up location (Richmond > Vancouver Broadway > East Vancouver > Burnaby)
        """
        cities = {"RM": 4, "VC": 3, "GD": 2, "BN": 1}
        output = []
        for key, value in cities.items():
            try:
                city = self.driver.find_element_by_id(key)
                print(f"{key} is a location to pick up")
                output.append(key)
            except:
                print(f"{key} is not location to pick up")
                continue
        try:
            options = {key: cities[key] for key in output}
            chosen_location = max(options, key=options.get)
        except:
            print("No locations in the Lower Mainland (except for coquitlam)")

        return chosen_location

    def auto_purchase(self):
        """Purchase Product"""

        # Open Browser
        self.open_browser()

        # Accept Cookies
        self.clickable_id("privacy-btn")

        # Add Product to Cart
        self.clickable_id("btn-addCart")

        # # Check out item
        self.clickable_id("btn-checkout")

        # Login
        self.login("lo-username", username=MY_ACC)
        self.login("lo-password", password=MY_PW)

        self.clickable_id("cm-btn-login")

        # proceed to checkout
        self.clickable_css(".btn.bg-green.text-white.font-1.text-center.f-500.py-1")

        # choose pickup
        self.clickable_id("ch-shipto-store")

        # Pick Richmond > East Broadway > East Vancouver > Burnaby
        location = self.pick_city()
        self.clickable_id(location)

        # proceed to next with pickup/chosen city (Shipping(1))
        self.clickable_css(".btn.navigation.float-right.bg-primary.text-white")

        # proceed to next (Payment(3))
        self.clickable_css(".btn.navigation.float-right.bg-primary.text-white")


def main(url):
    cc = CanadaComputers(url, MY_ACC, MY_PW)
    cc.auto_purchase()


if __name__ == "__main__":
    try:
        main(this_url)
    except Exception as e:
        print(str(e))
