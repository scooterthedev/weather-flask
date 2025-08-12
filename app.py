from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")
URL = "https://api.tomorrow.io/v4/weather/realtime"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/get-location', methods=['POST'])
def location():
    city = request.form.get('city')
    if not city:
        return render_template('index.html', error=True)
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        geo_resp = requests.get(geo_url).json()

        if "results" in geo_resp and len(geo_resp["results"]) > 0:
            lat = geo_resp["results"][0]["latitude"]
            lon = geo_resp["results"][0]["longitude"]
            return redirect(url_for('weather', city=city, lat=lat, lon=lon))
        else:
            print(f"No city found")
            return render_template('index.html', error=True)

    except Exception as e:
        print(f"Error occurred: {e}")
        return render_template('index.html', error=True)

@app.route('/get-weather', methods=['GET'])
def weather():
    city = request.args.get('city')
    lat = request.args.get('lat')
    lon = request.args.get('lon')


    if not (city and lat and lon):
        return render_template("index.html", error=True)
    
    try:
        params = {
            "location": f"{lat},{lon}",
            "apikey": API_KEY
        }
        resp = requests.get(URL, params=params).json()

        weather_data = {
            "city": city.title(),
            "temperature": resp["data"]["values"]["temperature"],
            "description": resp["data"]["values"]["weatherCode"],
        }
        return render_template("index.html", weather=weather_data)
    except Exception as e:
        print(f"Error yay!")
        return render_template("index.html", error=True)



if __name__ == '__main__':
    app.run(port=5000, debug=True)