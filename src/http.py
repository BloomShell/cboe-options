#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__      = "Bloomshell"

import requests
import logging 
from typing import Dict, Optional

class ResponseError(Exception):
    """
    Custom exception to handle HTTP response errors.

    Attributes:
    - status_code (int): HTTP status code of the response.
    - message (str): Error message.
    """
    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(f"HTTP {status_code}: {message}")
        self.status_code = status_code
        self.message = message

def get(
    url: str,
    params: Optional[Dict] = None,
    agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    accept: str = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
) -> requests.Response:
    """
    Sends an HTTP GET request to the specified URL with optional query parameters and custom headers.

    Parameters:
    - url (str): The URL to which the GET request is sent.
    - params (dict, optional): A dictionary of query parameters to include in the request. Default is None.
    - agent (str, optional): The User-Agent string to use in the request header. Default is a common Firefox user agent.
    - accept (str, optional): The Accept header string specifying the types of content that can be accepted. Default is a common browser's accept header.

    Returns:
    - requests.Response: The response object resulting from the GET request.

    Raises:
    - ResponseError: If the response status code indicates an error (e.g., 4xx or 5xx).

    Example Usage:
    response = request(
        url="https://api.example.com/data",
        params={"key1": "value1", "key2": "value2"},
        agent="Mozilla/5.0 (compatible; MyBot/0.1; +http://mybot.example.com/bot)",
        accept="application/json"
    )
    """
    try:
        response = requests.get(
            url=url,
            params=params,
            timeout=100,
            headers={
                "User-Agent": agent,
                "Accept": accept
            }
        )
        # Check if the response is successful
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx and 5xx)

        # Log successful request
        logging.info(f"Successfully fetched data for URL: {url}")
        return response

    except requests.exceptions.HTTPError as http_err:
        # Log and raise a custom exception for HTTP errors
        logging.error(f"HTTP error occurred for URL: {url} - Status Code: {response.status_code} - {http_err}")
        raise ResponseError(response.status_code, str(http_err))

    except Exception as err:
        # Log and raise a custom exception for other errors
        logging.error(f"An error occurred while fetching URL: {url} - {err}")
        raise ResponseError(0, str(err))  # Status code 0 for non-HTTP errors
    