from enum import Enum

GOOGLE_API = "GOOGLE_API"
SMARTY_ID ="Smarty_AuthID"
SMARTY_TOKEN = "Smarty_AuthToken"
Rapid_API_Key = "Rapid_API_Key"
Rapid_API_Host = "RapidAPI_Host"
Gkey = GOOGLE_API
CityDB = "city_cache.txt"
CityZipcodes = "zipcode_cache.txt"
Results_json = "results.txt"
Result_Output = "results.xlsx"
RedLineHost = "RedLine_Host"
target_travel_time = 45
RawCityData = {}
threads_complete = 0
zip_codes_acquired = False
lost_cities = []

States = {
"Alabama":	"AL",
"Alaska":	"AK",
"Arizona":	"AZ",
"Arkansas":	"AR",
"California":	"CA",
"Colorado":	"CO",
"Connecticut":	"CT",
"Delaware":	"DE",
"Florida":	"FL",
"Georgia":	"GA",
"Hawaii":	"HI",
"Idaho":	"ID",
"Illinois":	"IL",
"Indiana":	"IN",
"Iowa":	"IA",
"Kansas":	"KS",
"Kentucky":	"KY",
"Louisiana":	"LA",
"Maine":	"ME",
"Maryland":	"MD",
"Massachusetts":	"MA",
"Michigan":	"MI",
"Minnesota":	"MN",
"Mississippi":	"MS",
"Missouri":	"MO",
"Montana":	"MT",
"Nebraska":	"NE",
"Nevada":	"NV",
"New Hampshire":	"NH",
"New Jersey":	"NJ",
"New Mexico":	"NM",
"New York":	"NY",
"North Carolina":	"NC",
"North Dakota":	"ND",
"Ohio":	"OH",
"Oklahoma":	"OK",
"Oregon":	"OR",
"Pennsylvania":	"PA",
"Rhode Island":	"RI",
"South Carolina":	"SC",
"South Dakota":	"SD",
"Tennessee":	"TN",
"Texas":	"TX",
"Utah":	"UT",
"Vermont":	"VT",
"Virginia":	"VA",
"Washington":	"WA",
"West Virginia":	"WV",
"Wisconsin":	"WI",
"Wyoming":	"WY",
}

