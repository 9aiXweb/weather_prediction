import requests
import geocoder
import json
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

city_list = []
weather_list = []
temp_list = []

def get_info_details(ip_addr):
    # Replace 'your_api_key' with your actual API key
    api_key = '84106a85dbecc8'
    url = f"https://ipinfo.io/{ip_addr}?token={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        info = {
            'ip': data.get('ip'),
            'hostname': data.get('hostname'),
            'city': data.get('city'),
            'region': data.get('region'), 
            'country': data.get('country'),
            'loc': data.get('loc'),
            'org': data.get('org'),
            'postal': data.get('postal'),
            'timezone': data.get('timezone'),
            'asn': data.get('asn'),
            'company': data.get('company'),
            'privacy': data.get('privacy'),
            'abuse': data.get('abuse')
        }
        return info  # 'org' usually contains the ISP information
    else:
        return "ISP information not available"

@app.route('/', methods=['GET', 'POST'])
def index():
    API_KEY = "cb244b3767f2404bfebbbeaa1c3f7d4e"  
    # response = requests.get('https://api.ipify.org?format=json')
    # if response.status_code == 200:
    #     ip_address = response.json()['ip']
    # ip_address = request.remote_addr
    client_ip = request.remote_addr  # クライアントのIPアドレスを取得

    response = requests.get(f'https://api.ipify.org?format=json&ip={client_ip}')
    data = response.json()

    # 必要な位置情報を取得
    ip_address =  request.headers.get('X-Forwarded-For', request.remote_addr)
    ip_list = ip_address.split(", ")
    ip_address = ip_list[0]
    # city = geocoder.ip(ip_address).city
    info = get_info_details(ip_address)
    city = info['city']

    if info is not None:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()

        # Extract weather info if the API call is successful, else error
        if data['cod'] == '404':
            return render_template('index.html', info=info, city_list=None, weather_list=None, temp_list=None)
            # return render_template('index.html', city_list=None, weather_list=None, temp_list=None, 
            #                        ip=info['ip'], hostname=info['hostname'], 
            #                        city=info['city'], region=info['region'], country=info['country'],
            #                        log=info['loc'], org=info['org'], postal=info['postal'],
            #                        timezone=info['timezone'], asn=info['asn'], company=['company'],
            #                        privacy=info['privacy'], abs=info['abs'],
            #                        )
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

            return render_template('index.html', info=info, city_list=None, weather_list=None, temp_list=None)
    
    elif request.method == 'POST':
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

        return render_template('index.html', info=info, city_list=None, weather_list=None, temp_list=None)
    else: return render_template('index.html', info=info, city_list=None, weather_list=None, temp_list=None)


if __name__ == '__main__':
    app.run(host='0.0.0.0') 

