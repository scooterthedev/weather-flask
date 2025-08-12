from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")
URL = "https://api.tomorrow.io/v4/weather/realtime"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-location', methods=['POST'])
def location():
    if request.method == 'POST':
        city = request.form.get('city')
        try:
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
            geo_resp = requests.get(geo_url).json()

            if "results" in geo_resp and len(geo_resp["results"]) > 0:
                lat = geo_resp["results"][0]["latitude"]
                lon = geo_resp["results"][0]["longitude"]

            else:
                print(f"No city found")

        except Exception as e:
            print(f"Error occurred: {e}")

    return lat, lon


@app.route('/get-weather', methods=['GET'])
def weather(lat, long):
    weather_data = None

    params = {
        "location": f"{lat},{lon}",
        "apikey": API_KEY
    }
    resp = requests.get(URL, params=params).json()

    weather_data = {
        "city": city.title(),
        "temperature": resp["data"]["value"]["temperature"],
        "description": resp["data"]["value"]["weatherCode"],
    }

    return render_template("index.html", weather=weather_data)



if __name__ == '__main__':
    app.run(port=5000, debug=True)