import requests
ip_addr = "116.94.143.13"
api_geolocation = 'e09ab315a1e64d67a73ce8bf111b5e55'

url = f"https://api.ipgeolocation.io/ipgeo?apiKey={api_geolocation}&ip={ip_addr}"
response2 = requests.get(url)


if response2.status_code == 200:
    data2 = response2.json()
    print(data2['languages'])