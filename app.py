import requests
import geocoder
import json
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

city_list = []
weather_list = []
temp_list = []


API_KEY = "cb244b3767f2404bfebbbeaa1c3f7d4e"  

@app.route('/', methods=['GET', 'POST'])
def index():
    ip_address = request.remote_addr
    city = geocoder.ip(ip_address)
    if request.method == 'POST':
        # with open('data/data.json', encoding='utf-8') as f:
        #     previous_data = json.load(f)
        # if(city is None and previous_data is None):
        #     return render_template('index.html')
        # if(previous_data is not None):
        #     city_list = previous_data["city"]
        #     weather_list = previous_data["weather"]
        #     temp_list = previous_data["temp"]

        # url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        # data = requests.get(url).json()

        # # Extract weather info if the API call is successful, else error
        # if data['cod'] == '404':
        #     return render_template('index.html', city_list=city_list, weather_list=weather_list, temp_list=temp_list)
        # else:
        #     weather = data['weather'][0]['description']
        #     temp = data['main']['temp']
        #     city_list.append(city)
        #     weather_list.append(weather)
        #     temp_list.append(temp)

        #     data_json = {
        #         'city': city_list,
        #         'weather': weather_list,
        #         'temp':temp_list
        #     }
        #     with open('data/data.json', 'w') as f:
        #         json.dump(data_json, f, indent=3)

        return render_template('index.html', city_list=None, weather_list=None, temp_list=None)

    else:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()

        # Extract weather info if the API call is successful, else error
        if data['cod'] == '404':
            return render_template('index.html', city_list=None, weather_list=None, temp_list=None)
        else:
            weather = data['weather'][0]['description']
            temp = data['main']['temp']
            city_list.append(city)
            weather_list.append(weather)
            temp_list.append(temp)

            data_json = {
                'city': city_list,
                'weather': weather_list,
                'temp':temp_list
            }
            with open('data/data.json', 'w') as f:
                json.dump(data_json, f, indent=3)

        return render_template('index.html', city_list=city_list, weather_list=weather_list, temp_list=temp_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0') 

