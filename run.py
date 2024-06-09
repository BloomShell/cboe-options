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
from jinja2 import Template
from email.mime.text import MIMEText
from src.http import get, ResponseError
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
SMTP_SERVER = "smtp.gmail.com"
PORT = 465
SENDER = "imlovingbees@gmail.com"
PASSWORD = "nphkbqpfxhnjzlqq"

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

    # Get the number of symbols (directories) in the options directory
    num_symbols = len(os.listdir("../hub/options"))

    # Get the number of JSON files in the options directory
    num_files = len(glob.glob("../hub/options/*/*.json"))

    # Load the HTML template for the email content
    content = open(r"../static/templates/newsletter.html").read()

    # Render the template with data
    template = Template(content)
    content = template.render(
        num_symbols=num_symbols,
        num_files=num_files
    )

    # Create the email message
    msg = MIMEMultipart()
    msg['Subject'] = f"Options Data from CBOE Website {time.asctime()}"
    msg['From'] = 'imlovingbees@gmail.com'

    # List of recipients
    recipients = ['pietroamin.puddu@gmail.com'] #, 'r.pauselli998@gmail.com'
    msg['To'] = ", ".join(recipients)

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Attach the HTML content to the email message
    msg.attach(MIMEText(content, 'html'))

    # Attach the log file
    log_file_path = "log/cboe-options.log"
    log_part = MIMEApplication(open("log\cboe-options-10062024.log", 'rb').read(), Name=os.path.basename(log_file_path))
    log_part['Content-Disposition'] = f'attachment; filename="{os.path.basename(log_file_path)}"'
    msg.attach(log_part)

    # Send the email using SMTP over SSL
    with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
        # Login to the SMTP server
        server.login(SENDER, PASSWORD)
        
        # Send the email to the recipients
        server.sendmail(msg['From'], recipients, msg.as_string())