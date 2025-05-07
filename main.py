from flask import Flask, render_template, request, jsonify, session, redirect, url_for, make_response
from tinydb import TinyDB, Query, where
from datetime import datetime, timedelta
import os
import requests
from geopy.geocoders import Nominatim

app = Flask(__name__)

@app.route("/",methods=["GET" , "POST"])
def traffic():
    def get_city_coordinates(city_name):
        geocode_url = f"https://nominatim.openstreetmap.org/search?city={city_name}&format=json&addressdetails=1"
        response = requests.get(geocode_url)
        
        # Check if the response was successful
        if response.status_code != 200:
            print(f"Error: Unable to fetch data from Nominatim API. Status Code: {response.status_code}")
            return None
        
        try:
            data = response.json()
        except ValueError as e:
            print(f"Error decoding JSON response: {e}")
            print(f"Raw response: {response.text}")
            return None
        
        if data:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            return lat, lon
        else:
            print(f"City {city_name} not found.")
            return None

    # Function to generate a bounding box around the city
    def generate_bbox(lat, lon, delta=0.01):  # delta controls the size of the bounding box
        # Calculate a simple bounding box around the coordinates
        min_lat = lat - delta
        max_lat = lat + delta
        min_lon = lon - delta
        max_lon = lon + delta
        
        return min_lon, min_lat, max_lon, max_lat

    # Get city coordinates for a given city
    city_name = "Amsterdam"
    coordinates = get_city_coordinates(city_name)

    if coordinates:
        lat, lon = coordinates
        # Generate the bounding box for the city
        bbox = generate_bbox(lat, lon)

        # Prepare the TomTom Traffic API request
        url = "https://api.tomtom.com/traffic/services/5/incidentDetails"
        params = {
            "key": "lEuvMGG2ZuFnmWmToohPF6JWSXKn7JSI",
            "bbox": f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}",
            "fields": """{incidents{type,geometry{type,coordinates},properties{id,iconCategory,magnitudeOfDelay,events{description,code,iconCategory},startTime,endTime,from,to,length,delay,roadNumbers,timeValidity,probabilityOfOccurrence,numberOfReports,lastReportTime,tmc{countryCode,tableNumber,tableVersion,direction,points{location,offset}}}}}""",
            "language": "en-GB",
            "timeValidityFilter": "present"
        }

        # Make the API request and get the response
        response = requests.get(url, params=params)

        # Check if the response was successful
        if response.status_code != 200:
            print(f"Error: Unable to fetch traffic data. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
        else:
            # Print the response
            try:
                traffic_data = response.json()
                print(traffic_data)
            except ValueError as e:
                print(f"Error decoding JSON response: {e}")
                print(f"Raw response: {response.text}")
    else:
        print("City coordinates not found.")
    return render_template("index.html")


"""
iconCategory	Incident Type
0	Traffic Jam
1	Accident
2	Roadwork
3	Hazard
4	Weather Condition
5	Traffic Regulation
6	Closed Road
7	Event or Incident
8	Unspecified Issue


"""



if __name__ == '__main__':
    app.run(debug=True)
