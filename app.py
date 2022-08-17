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



def Cache_Results():
   try:
      with open('results.txt','w') as res:
         resultObj = json.dumps(RawCityData)
         res.write(resultObj)
   except Exception as error:
      logging.error(error)

def Cache_City_Json(cities:list):
   logging.info(f"Storing cities in {CityDB}")
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
         RawCityData = deepcopy(obj)
   except Exception as e:
      logging.error("Unable to read cached data.",e)

def Compile_City_Json():
   """Query Rapid Api for a list of cities based on the input state"""
   cityDirectory = os.path.join(os.path.dirname(__file__),CityDB)
   try:
      if not os.path.exists(cityDirectory) or os.stat(cityDirectory).st_size <= 2:
         if len(sys.argv[1]) < 3:
            raise ValueError("ValueError: Input State needs to be spelled out")
      # if not os.path.exists(cityDirectory) or os.stat(cityDirectory).st_size == 0:
         print('No cache data exists. Querying API')
         url = 'https://andruxnet-world-cities-v1.p.rapidapi.com/'
         querystring = {"query":sys.argv[1],"searchby":"state"}
         headers = {'X-RapidAPI-Key': config(Rapid_API_Key),
                     'X-RapidAPI-Host': config(Rapid_API_Host)
                  }
         response = requests.get(url,headers=headers,params=querystring)
         cities = list(set([r['city'] for r in response.json()]))
         Cache_City_Json(cities)
      else:
         print(f'Reading data from city_cache. File Size: {os.stat(cityDirectory).st_size}')         
         Read_Cached_City_Data()
   except (Exception,ValueError) as e:
      print(e)
      logging.error(e)
   
def Retrieve_ZipCodeV2(city:str,options,currentIdx=0):
   global lost_cities
   global RawCityData

   if currentIdx > len(options) - 1:
      lost_cities.append(city)
      RawCityData['lost_cities'] = lost_cities
      return
   _city = city
   _state = States[options[currentIdx].title()]
   zipCodeDir = os.path.join(os.path.dirname(__file__),CityZipcodes)
   code = ""
   zipcodes = [""]
   with open(CityZipcodes,'r') as zips:
      try:
         zipObj = json.load(zips)
         zipCodeStored = 'zipcode' in zipObj[_city] and zipObj[_city]['zipcode'] is not None
         if zipCodeStored:
            code = zipObj[_city]['zipcode']
            RawCityData[_city]['zipcode'] = code 
            return
         else:
            logging.info(f"Code for {_city} not stored. Attempting to locate")
            url = f"https://redline-redline-zipcode.p.rapidapi.com/rest/city-zips.json/{_city}/{_state}"
            headers = {'X-RapidAPI-Key': config(Rapid_API_Key),'X-RapidAPI-Host': config(RedLineHost)}
            response = requests.get(url,headers=headers)
            if response.status_code == 200:
               zipcodes = response.json()['zip_codes']
            else:
               return
            try:
               code = zipcodes[0]
               RawCityData[_city]['zipcode'] = code
               print(f"Zip Code located for {_city} : {code}")
            except IndexError as e:
               Retrieve_ZipCodeV2(_city,options,currentIdx + 1)
               logging.error(e)
               logging.error('This city and state do not have a corresponding zipcode. Try another state.')
               logging.info(traceback.format_exc())
      except Exception as e:
         logging.info(traceback.format_exc())

def Cache_Zipcodes():
   try:
      with open(CityZipcodes,'w') as cityZipCodeData:
         json_obj = json.dumps(RawCityData,indent=4)
         cityZipCodeData.write(json_obj)
   except Exception as e:
      print("There was an issue writing to the cache",e)

def Compile_City_ZipCodes(cities,options):
   print("Checking for ZipCode")
   for c in cities:
      Retrieve_ZipCodeV2(c,options)
   
   print("Caching ZipCodes")
   Cache_Zipcodes()

def Compile_Distance_Travel():
   origin = sys.argv[2]
   cities = []
   print('Compiling travel time')
   print(f'Current RawCityData: {RawCityData}')
   cities = list(RawCityData.keys())
   for city in cities:
      if city == 'lost_cities':
         continue
      url = f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={city}&key={config(Gkey)}'
      response = requests.get(url).json()
      rows = response['rows']
      # print(f'Rows: {rows}')
      try:
         durationObj = rows[0]['elements'][0]['duration']
         if durationObj != None:
            duration = durationObj['text']
            RawCityData[city]['travel_time'] = duration
      except KeyError as k:
         logging.error(k)
         logging.error(traceback.format_exc())
   Cache_Results()

def Read_Results_File():
   try:
      with open(Results_json,'r') as result:
         obj = json.load(result) 
         return deepcopy(obj)
         
   except Exception as error:
      logging.error(error)

def remove(sheet,row):
   for cell in row:
      if cell.value != None:
         return
   sheet.delete_rows(row[0].row,1)

def Delete_Empty_Rows(worksheet):
   
   ws = worksheet

   for row in ws:
      remove(ws,row)
   
   for row in ws:
      for cell in row:
         if cell.value == None:
            Delete_Empty_Rows(ws)

def set_auto_width(worksheet):
   logging.info('Setting auto width')
   for col in worksheet.columns:
      max_length = 0
      column = col[0].column_letter
      for cell in col:
         if len(str(cell.value)) > max_length:
            max_length = len(str(cell.value))
      adjusted_width = max_length + (max_length * .3)
      worksheet.column_dimensions[column].width = adjusted_width

def filter_by_travel_time(worksheet):
   logging.info('Filtering Results based on Requested Travel Time')
   rows_to_remove = []
   for row in worksheet.iter_rows(min_row=2,min_col=3,max_col=3):
      for cell in row:
         travel_time = 0
         # split the string         
         arr = cell.value.split(' ')
         if len(arr) > 2:
            # Convert value at index 0 to minutes
            # add to value at index 2 if length > 2
            travel_time = (int(arr[0]) * 60) + int(arr[2])
         else:
            travel_time = int(arr[0])
         # Delete the row if not within our range
         if travel_time > target_travel_time:
            rows_to_remove.append((cell,cell.value))
   
   for i in rows_to_remove:
      worksheet.delete_rows(i[0].row,1)

def Format_Excel_Results(worksheet):
   set_auto_width(worksheet)
   filter_by_travel_time(worksheet)

def Export_To_Excel():
   logging.info('Preparing to Export Results')
   results_dict = Read_Results_File()
   wb = openpyxl.Workbook()
   sheet = wb.active
   headers = ["City","ZipCode","Travel Time"]
   keys = list(results_dict.keys())[:-1]

   for i in range(len(headers)):
      sheet.cell(row=1,column=i+1).value = headers[i]
   for i in range(len(keys)):
      city = keys[i]
      try:
         zipcode = results_dict[keys[i]]['zipcode']
         duration = results_dict[keys[i]]['travel_time']
         sheet.cell(row=2+i,column=1).value = city
         sheet.cell(row=2+i,column=2).value = zipcode
         sheet.cell(row=2+i,column=3).value = duration
      except KeyError as error:
         logging.info('Entry missing zipcode or duration...Ignoring')
         pass
   
   logging.info('Removing empty rows')
   Delete_Empty_Rows(sheet)
   logging.info('Formatting spreadsheet')
   Format_Excel_Results(sheet)
   logging.infor('Formatting Complete!')
   wb.save(Result_Output)

def run():
   if not os.path.exists(os.path.join(os.path.dirname(__file__),Results_json)):
      multiQuery = input('Do you want to include multiple states in this query (y/n): ')
      done = False
      options = []
      if multiQuery.lower() == 'y':
         while done == False:
            state = input('Enter the full state name. (Press q when done): ')
            if state.lower() == 'q':
               done = True
               break
            options.append(state)


      Compile_City_Json()
      keys = []
      with open(CityDB,'r') as cityDB:
         city_list = json.load(cityDB)
         keys = list(city_list.keys())
      Compile_City_ZipCodes(keys,options)
      Compile_Distance_Travel()
      Export_To_Excel()
   else:
      Export_To_Excel()

if __name__ == '__main__':
   logging.basicConfig(format='%(levelname)s:%(message)s',filename='events.log',level=logging.INFO)
   run()