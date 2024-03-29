import requests
import json
from flask import Flask, render_template, request


app = Flask(__name__)


def get_info_details(ip_addr):
    # Replace 'your_api_key' with your actual API key
    api_key = '84106a85dbecc8'
    api_geolocation = 'e09ab315a1e64d67a73ce8bf111b5e55'
    url = f"https://ipinfo.io/{ip_addr}?token={api_key}"
    response = requests.get(url)
    
    url = f"https://api.ipgeolocation.io/ipgeo?apiKey={api_geolocation}&ip={ip_addr}"
    response2 = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        data2 = response2.json()
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
            'temp': None,
            'weather':None,
            'language':data2['languages']
        }
        return info  # 'org' usually contains the ISP information
    else:
        return None

@app.route('/')
def index():
    API_KEY = "cb244b3767f2404bfebbbeaa1c3f7d4e"  
    client_ip = request.remote_addr  # クライアントのIPアドレスを取得

    response = requests.get(f'https://api.ipify.org?format=json&ip={client_ip}')
    data = response.json()

    # 必要な位置情報を取得
    ip_address =  request.headers.get('X-Forwarded-For', request.remote_addr)
    ip_list = ip_address.split(", ")
    print(ip_address)
    ip_address = ip_list[0]
    print(ip_address)
    info = get_info_details(ip_address)

    if info is not None:
        city = info['city']
        LATITUDE, LONGITUDE = info['loc'].split(',')
        
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()

        # Extract weather info if the API call is successful, else error
        if data['cod'] == '404':
            return render_template('index.html', info=info,  LATITUDE=LATITUDE, LONGITUDE=LONGITUDE
                                   )
        else:
            info['weather'] = data['weather'][0]['description']
            info['temp'] = str(data['main']['temp']) +"°c"
            
            return render_template('index.html', info=info,  LATITUDE=LATITUDE, LONGITUDE=LONGITUDE
                                   )  
    else: return render_template('index.html', info=None)
    # return render_template('index.html', info=None)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 
    # app.run(port=5000, debug=True) 

