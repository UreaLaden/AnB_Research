"""
Author: Leaundrae Mckinney
Date: 15 August 2022

The goal of this program is to accumulate a list of cities in Virginia
to target for rental arbitrage .
Input Argument minimum travel time in minutes and origin zip code

Resources: 
 - Every City in Virginia: https://www.virginia-demographics.com/cities_by_population
    ---- https://public.opendatasoft.com/api/records/1.0/search/?dataset=us-cities-demographics&q=&facet=city&facet=state&facet=race&refine.state={State Name}
 - Determines the zip code of a given city must include ,abbreviated state:     
    --API:  https://www.smarty.com/docs/sdk/python ******* 
    ----https://github.com/smartystreets/smartystreets-python-sdk/blob/master/examples/us_zipcode_single_lookup_example.py 
 - Time & Distance Matrix API: https://maps.googleapis.com/maps/api/distancematrix/json?origins={Origin ZipCode}&destinations={Destination ZipCode}&key={API Key}

 Process:
 - Check for a json file containing a list of every city in Virginia
 - If the list is not available we scrape the url and store the results
 - For each city on our list we acquire the zipcode
 - Once the zip codes are compiled we'll determine the distance and travel time
 - For all cities that fall within target travel time, we will highlight the entry

 
"""
from imports import *

Gkey = config(GOOGLE_API)
SAuthID = config(SMART_ID)
SToken = config(SMARTY_TOKEN)