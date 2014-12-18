import urllib
import json

def temperature(town):  # Takes a town as paramater and return it's temperature in C
    try:
        #Getting the JSON from openweathermap into a python dictionary
        url = "http://api.openweathermap.org/data/2.5/weather?q=" + town + "&units=metric"
        raw_json_weather = urllib.urlopen(url)
        weather_dic = json.loads(raw_json_weather.read())
    
    #Check existence of town and return temperature in C
        if weather_dic["cod"] == "404":
            return "Not Found"
        else:
            return str(int(weather_dic["main"]["temp"]))
    except:
            return "Error" #Error often happens when the town string given is too long