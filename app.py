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
from utils.imports import *

Gkey = config(GOOGLE_API)

def Cache_City_Json(cities:list):
   db = {}
   for c in cities:
      db[c] = {}
   
   try:
      with open(CityDB,'w') as cityDB:
         json_obj = json.dumps(db,indent=4)
         cityDB.write(json_obj)
   except Exception as e:
      logging.error("There was a problem attempting to write the object",e)

def Read_Cached_City_Data():
   global RawCityData
   try:
      with open(CityDB,'r') as cityData:
         obj = json.load(cityData)
         RawCityData = obj
   except Exception as e:
      logging.error("Unable to read cached data.",e)

def Compile_City_Json():
   """Query Rapid Api for a list of cities based on the input state"""
   cityDirectory = os.path.join(os.path.dirname(__file__),CityDB)
   if not os.path.exists(cityDirectory) or os.stat(cityDirectory).st_size == 0:
      print('No cache data exists. Querying API')
      url = 'https://andruxnet-world-cities-v1.p.rapidapi.com/'
      querystring = {"query":sys.argv[1],"searchby":"state"}
      headers = {'X-RapidAPI-Key': config(Rapid_API_Key),
                  'X-RapidAPI-Host': config(Rapid_API_Host)
               }
      response = requests.get(url,headers=headers,params=querystring).json()
      cities = list(set([r['city'] for r in response]))
      Cache_City_Json(cities)
   else:
      print('Reading data from city_cache')
      Read_Cached_City_Data()
   
def Retrieve_ZipCodeV2(city:str,state = sys.argv[1]):
   _city = city
   _state = state

   try:
      if _city in RawCityData:
         x = RawCityData[_city]['zipcode']
      return
   except KeyError as k:
      url = f"https://redline-redline-zipcode.p.rapidapi.com/rest/city-zips.json/{_city}/{_state}"
      headers = {'X-RapidAPI-Key': config(Rapid_API_Key),
                     'X-RapidAPI-Host': config(RedLineHost)
                  }
      response = requests.get(url,headers=headers)
      zipcodes = response.json()['zip_codes']
      if len(zipcodes) > 0:
         RawCityData[_city]['zipcode'] = zipcodes[0]
      
   Cache_Zipcodes()


def Cache_Zipcodes():
   global RawCityData
   try:
      with open(CityDB,'w') as cityData:
         json_obj = json.dumps(RawCityData,indent=4)
         cityData.write(json_obj)
   except Exception as e:
      print("There was an issue writing to the cache",e)
   
   Read_Cached_City_Data()

def Compile_City_ZipCodes():
   cities = list(RawCityData.keys())
   for c in cities:
      Retrieve_ZipCodeV2(c)
      Retrieve_ZipCodeV2(c,'wv') #TODO need a way to make this optional depending on user input
   Cache_Zipcodes()

def Compile_Distance_Travel():
   origin = sys.argv[2]
   cities = []
   print('Compiling travel time')
   try:
      with open (CityDB) as cityData:
         newObj = json.load(cityData)
         RawCityData = newObj
         cities = list(RawCityData.keys())
         for city in cities:
            destination = city['zipcode']
            url = f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&key={Gkey}'
            response = requests.get(url).json()
            duration = response['rows'][0]['elements'][0]['duration']['text']
            if duration != None:
               RawCityData[city]['travel_time'] = duration
   except Exception as e:
      print("Something went terribly wrong: ",e)
   
   Cache_City_Json(cities)

def Export_To_Excel():
   pass

def Format_Excel_Results():
   pass

def run():
   # Compile_City_Json()
   # Compile_City_ZipCodes()
   Compile_Distance_Travel()

if __name__ == '__main__':
   logging.basicConfig(format='%(levelname)s:%(message)s',filename='events.log',level=logging.INFO)
   run()