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

# Richmond -> data-store-name="Richmond" id ="RM"
# Vancouver Broadway -> data-store-name="Vancouver Broadway" id="VC"
# East Vancouver -> data-store-name="East Vancouver" id="GD"
# Burnaby -> data-store-name="Burnaby" id="BN"


class CanadaComputers:
    """Purchases specified item from https://www.canadacomputers.com/

    Attributes:
        url: url of item
        user: username of canadac computers account
        pw: password of canadac computers account

    """

    def __init__(self, url, user, pw):
        """Initialize CanadaComputers Object"""
        self.url = url
        self.user = user
        self.pw = pw
        self.driver = webdriver.Chrome()

    def open_browser(self):
        self.driver.maximize_window()
        self.driver.get(self.url)

    def clickable_id(self, _id):
        element = WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable((By.ID, _id))
        )

        element.click()

    def clickable_css(self, _css):
        element = WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, _css))
        )

        element.click()

    def login(self, tag, username=None, password=None):
        input_ = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.ID, tag))
        )

        if username != None:
            input_.send_keys(self.user)
        elif password != None:
            input_.send_keys(self.pw)


def main(url):
    cc = CanadaComputers(url, MY_ACC, MY_PW)

    # Open Browser
    cc.open_browser()

    # Accept Cookies
    cc.clickable_id("privacy-btn")

    # Add Product to Cart
    cc.clickable_id("btn-addCart")

    # # Check out item
    cc.clickable_id("btn-checkout")

    # Login
    cc.login("lo-username", username=MY_ACC)
    cc.login("lo-password", password=MY_PW)

    cc.clickable_id("cm-btn-login")

    # proceed to checkout
    cc.clickable_css(".btn.bg-green.text-white.font-1.text-center.f-500.py-1")

    # choose pickup
    cc.clickable_id("ch-shipto-store")

    # Pick Richmond > East Broadway > East Vancouver > Burnaby
    cc.clickable_id("RM")

    # proceed to next with pickup/chosen city (Shipping(1))
    cc.clickable_css(".btn.navigation.float-right.bg-primary.text-white")

    # proceed to next (Payment(3))
    cc.clickable_css(".btn.navigation.float-right.bg-primary.text-white")


if __name__ == "__main__":
    try:
        main(this_url)
    except Exeception as e:
        print(str(e))
