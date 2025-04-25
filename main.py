from flask import Flask, render_template, request, jsonify, session, redirect, url_for, make_response
from tinydb import TinyDB, Query, where
from datetime import datetime, timedelta
import os
import requests

app = Flask(__name__)

@app.route("/",methods=["GET" , "POST"]) #NE DELA NITI MAL
def weatherFor():

    apiKey = "8d80c9afce8da5a191e74cb02596e828"
    mesto = "Ljubljana"
    print(mesto)
    apiCall = f"https://api.openweathermap.org/data/2.5/forecast?q={mesto}&appid={apiKey}&units=metric"
    response = requests.get(apiCall)
    dataF = response.json()


    today = datetime.today().date()
    tommorow = today + timedelta(days=1)
    dayAfterTom = today + timedelta(days=2)


    def getDate(index):
        dt = datetime.strptime(dataF["list"][index-1]["dt_txt"], "%Y-%m-%d %H:%M:%S")
        date_only = dt.date()
        return date_only

    def getUra(index):
        dt = datetime.strptime(dataF["list"][index-1]["dt_txt"], "%Y-%m-%d %H:%M:%S")
        time_only = dt.time()
        return time_only
    
    index = 0

    forToday = {}
    forTommorow = {}
    forDayAftrTom = {}

    for vremeU in dataF["list"]:
        index += 1
        dan = getDate(index)
        if today == dan:
            print("---------------------------DANES----------------------------")
            
            vremeFor = {
                "čas" : dataF["list"][index-1]["dt_txt"],
                "temp" : dataF["list"][index-1]["main"]["temp"],
                "status": dataF["list"][index-1]["weather"]["main"],
                "wind": dataF["list"][index-1]["wind"]["speed"]
            }

            forToday[f"{getUra(index)}"] = vremeFor

            print(forToday)
        
        elif tommorow ==  dan:
            print("---------------------------TOMMOROW----------------------------")


        elif dayAfterTom ==  dan:
            print("---------------------------DAY AFTER TOMMOROW----------------------------")







    '''dan1 = {
        "ura1": {
            "čas" : dataF["list"][0]["dt_txt"],
            "temp" : dataF["list"][0]["main"]["temp"],
            "status": dataF["list"][0]["weather"]["main"],
            "wind": dataF["list"][0]["wind"]["speed"]
        },
        "ura2" : {
            "čas" : dataF["list"][1]["dt_txt"],
            "temp" : dataF["list"][1]["main"]["temp"],
            "status": dataF["list"][1]["weather"]["main"],
            "wind": dataF["list"][1]["wind"]["speed"]
        }
    }
    dan2 = {
        "ura1": {
            "čas" : dataF["list"][4]["dt_txt"],
            "temp" : dataF["list"][4]["main"]["temp"],
            "status": dataF["list"][4]["weather"]["main"],
            "status": dataF["list"][4]["wind"]["speed"]
        },
        "ura2" : {
            "čas" : dataF["list"][5]["dt_txt"],
            "temp" : dataF["list"][5]["main"]["temp"],
            "status": dataF["list"][5]["weather"]["main"],
            "status": dataF["list"][5]["wind"]["speed"]
        }
    }'''    

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
