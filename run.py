#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
===============================================================================
CBOE-Options
===============================================================================

Fetches options data for symbols from the CBOE website, 
saves it as JSON files, and logs the process.

This function retrieves options data for symbols from the CBOE website, 
saves it as JSON files, and logs the process.
It iterates over each symbol, makes an HTTP GET request from the CBOE API, 
and saves the response JSON data to a file.
It logs information about the success or failure of each request.

Usage: run.py [options]
Options:
    -h, --help       Display this help message
    -d, --docs       Display documentation

===============================================================================
"""

__author__ = "Bloomshell"

import re
import ssl
import sys
import time
import glob
import smtplib
import logging
import datetime
import os, json
import pandas as pd
import multiprocessing
from jinja2 import Template
from joblib import delayed, Parallel
from email.mime.text import MIMEText
from src.http import get, ResponseError
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

SMTP_SERVER = "smtp.gmail.com"
PORT = 465
SENDER = "imlovingbees@gmail.com"
PASSWORD = "nphkbqpfxhnjzlqq"


def worker(symbol: str):
    # Ensure symbol is stripped of whitespace and in uppercase
    symbol = symbol.strip().upper()

    for variation in [symbol, f"_{symbol}"]:
        try:
            # Make HTTP GET request to fetch options data
            response = get(
                f"https://cdn.cboe.com/api/global/delayed_quotes/options/{variation}.json"
            )

            # Create directory to save options data, if not exists
            os.makedirs(f"hub/options/{variation}", exist_ok=True)

            # Save response JSON data to file
            json.dump(
                response.json(),
                open(f"hub/options/{variation}/options-chain-{variation}-{quotedate}.json", "w"),
            )

            # Log success message
            logging.info(
                f"Data received and saved at @root:hub/options/{variation}/options-chain-{variation}-{quotedate}.json"
            )

            # Exit variations
            break

        except ResponseError as e:
            # Log warning message for response error
            logging.warning(f"Failed to fetch data for symbol: {variation} - {e}")

        except Exception as e:
            # Log critical message for unexpected errors
            logging.critical(f"Unhandled exception for symbol: {variation} - {e}")


if __name__ == "__main__":

    if len(sys.argv) > 1 and (sys.argv[1] in ["-d", "--docs", "--d"]):
        # Display documentation
        print(__doc__)
        sys.exit(0)

    # Get the directory of the Python file
    file_dir = os.path.dirname(os.path.realpath(__file__))

    # Change the current directory to the directory of the Python file
    os.chdir(file_dir)

    # Get the current date in the format 'ddmmyyyy'
    rundate = datetime.datetime.today().strftime("%d%m%Y")

    # Get the quote date in the format 'ddmmyyyy'
    quotedate = datetime.datetime.now() - datetime.timedelta(days=1)
    if quotedate.strftime('%A') in ['Saturday', 'Sunday']: sys.exit(0)
    else: quotedate = quotedate.strftime("%d%m%Y")

    # Create directory to save log data, if not exists
    os.makedirs(f"log", exist_ok=True)

    # Configure logging
    logging.basicConfig(
        filename=f"log/cboe-options-{rundate}.log",  # Log file to store logs
        level=logging.INFO,  # Log level
        format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    )

    # Try to fetch the list of symbols directly from the CBOE website
    try:
        symbols = pd.read_html(
            "https://www.cboe.com/us/options/market_statistics/post_and_station/"
        )[0]["Underlying"].to_list()
        
        # Join the list elements with a comma and write to the file
        open("meta/symbols.txt", 'w').write(",".join(symbols))

    except Exception as e:
        # If the fetch fails, fallback to the local file
        # Load symbols from the file
        symbols = open("meta/symbols.txt").read().strip().split(",")
    
    # Use joblib.Parallel and joblib.delayed  
    Parallel(n_jobs=-1)(delayed(worker)(symbol) for symbol in symbols)   
