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

__author__      = "Bloomshell"

import ssl
import sys
import time
import glob
import smtplib
import logging
import datetime
import os, json
from src.http import get, ResponseError


if __name__ == "__main__":

    if len(sys.argv) > 1 and (sys.argv[1] in ['-d', '--docs', "--d"]):
        # Display documentation
        print(__doc__)
        sys.exit(0)

    # Get the directory of the Python file
    file_dir = os.path.dirname(os.path.realpath(__file__))

    # Change the current directory to the directory of the Python file
    os.chdir(file_dir)

    # Get the current date in the format 'ddmmyyyy'
    sd = datetime.datetime.today().strftime("%d%m%Y")

    # Create directory to save log data, if not exists
    os.makedirs(f"log", exist_ok=True)

    # Configure logging
    logging.basicConfig(
        filename=f'log/cboe-options-{sd}.log',  # Log file to store logs
        level=logging.INFO,            # Log level
        format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
    )

    # Load symbols from the file
    symbols = open("meta/symbols.txt").read().strip().split(",")

    # Iterate over each symbol and request data
    for symbol in symbols:
        # Ensure symbol is stripped of whitespace and in uppercase
        symbol = symbol.strip().upper()

        try:
            # Make HTTP GET request to fetch options data
            response = get(f"https://cdn.cboe.com/api/global/delayed_quotes/options/{symbol}.json")

            # Create directory to save options data, if not exists
            os.makedirs(f"hub/options/{symbol}", exist_ok=True)

            # Save response JSON data to file
            json.dump(response.json(), open(f"hub/options/{symbol}/options-chain-{symbol}-{sd}.json", 'w'))

            # Log success message
            logging.info(f"Data received and saved at @root:hub/options/{symbol}/options-chain-{symbol}-{sd}.json")

        except ResponseError as e:
            # Log warning message for response error
            logging.warning(f"Failed to fetch data for symbol: {symbol} - {e}")

        except Exception as e:
            # Log critical message for unexpected errors
            logging.critical(f"Unhandled exception for symbol: {symbol} - {e}")
