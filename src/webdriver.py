#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provides a utility class for interacting with web pages using Selenium WebDriver.

Usage:
    from webdriver import WebDriver

    # Create a WebDriver instance
    wd = WebDriver()

    # Load a web page
    wd.get("https://example.com")

    # Click an element
    wd.click("//button[@id='submit']")

    # Send keys to an input field
    wd.sendKeys("//input[@name='username']", "user@example.com")
"""

__author__      = "Bloomshell"

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import warnings
import bs4


class WebDriver(object):
    """
    A custom wrapper class for managing and interacting with a Chrome WebDriver.
    This class provides methods for common browser actions like navigating to a URL,
    interacting with web elements (clicking, sending keys), and retrieving page content
    as BeautifulSoup objects.
    """

    def __init__(
        self, service_path: str
    ) -> None:
        """
        Initializes the WebDriver instance with the specified ChromeDriver executable path.
        It sets the browser window size and maximizes the window.

        Parameters:
        - service_path (str): Path to the ChromeDriver executable.
        """
        # Initialize the Chrome WebDriver service with the provided path.
        self.driver = webdriver.Chrome(service=Service(service_path))
        # Set the initial window size to 1024x600.
        self.driver.set_window_size(1024, 600)
        # Maximize the browser window.
        self.driver.maximize_window()

    def get(self, url: str) -> bool:
        """
        Navigates the browser to the specified URL.

        Parameters:
        - url (str): The URL to navigate to.

        Returns:
        - bool: True if navigation was successful, False if it failed.
        """
        try:
            # Attempt to open the URL.
            self.driver.get(url)
            return True
        except WebDriverException:
            # Warn and return False if the navigation fails.
            warnings.warn("WebDriver.get(...) Failed.")
            return False

    def getSoup(self) -> str:
        """
        Retrieves the current page source and parses it as a BeautifulSoup object.

        Returns:
        - BeautifulSoup object: Parsed HTML of the current page using 'lxml' parser.
        """
        # Parse the page source using BeautifulSoup and return it.
        return bs4.BeautifulSoup(self.driver.page_source, "lxml")

    def timedClick(self, xpath: str, timeout: int = 60) -> bool:
        """
        Clicks on an element specified by the XPath after waiting for it to be clickable,
        with a specified timeout.

        Parameters:
        - xpath (str): The XPath of the element to click.
        - timeout (int): Maximum time to wait (in seconds) for the element to be clickable.

        Returns:
        - bool: True if the click action was successful, False if it failed.
        """
        try:
            # Wait until the element is clickable and then perform the click.
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            ).click()
            return True
        except WebDriverException:
            # Warn and return False if the click action fails.
            warnings.warn(f"WebDriver.timedClick({xpath}) Failed.")
            return False

    def click(self, xpath: str) -> bool:
        """
        Immediately clicks on an element specified by the XPath without waiting.

        Parameters:
        - xpath (str): The XPath of the element to click.

        Returns:
        - bool: True if the click action was successful, False if it failed.
        """
        try:
            # Attempt to find the element by XPath and click it.
            self.driver.find_element(By.XPATH, xpath).click()
            return True
        except WebDriverException:
            # Warn and return False if the click action fails.
            warnings.warn(f"WebDriver.click({xpath}) Failed.")
            return False

    def sendKeys(self, xpath: str, keys: str) -> bool:
        """
        Sends a sequence of keys to an element specified by the XPath.

        Parameters:
        - xpath (str): The XPath of the element to send keys to.
        - keys (str): The keys to be sent to the element.

        Returns:
        - bool: True if sending keys was successful, False if it failed.
        """
        try:
            # Attempt to find the element by XPath and send the specified keys.
            self.driver.find_element(By.XPATH, xpath).send_keys(keys)
            return True
        except WebDriverException:
            # Warn and return False if sending keys fails.
            warnings.warn(f"WebDriver.sendKeys({xpath}, {keys}) Failed.")
            return False
