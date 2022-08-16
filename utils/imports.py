import requests,sys,json,logging,os
from utils.constants import *
from decouple import config
from smartystreets_python_sdk import StaticCredentials, exceptions,ClientBuilder
from smartystreets_python_sdk.us_zipcode import Lookup as ZIPCodeLookup