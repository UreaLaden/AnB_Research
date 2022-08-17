import requests,sys,json,logging,os
from utils.constants import *
from decouple import config
from smartystreets_python_sdk import StaticCredentials, exceptions,ClientBuilder
from smartystreets_python_sdk.us_zipcode import Lookup as ZIPCodeLookup
from threading import Thread
from copy import deepcopy
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import traceback
import openpyxl