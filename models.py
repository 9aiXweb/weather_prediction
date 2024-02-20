    ip_addr = "8.8.8.8"
    api_geolocation = 'e09ab315a1e64d67a73ce8bf111b5e55'
    url = f"https://ipinfo.io/{ip_addr}?token={api_key}"
    response = requests.get(url)
    data = response.json()
    
    url = f"https://api.ipgeolocation.io/ipgeo?apiKey={api_geolocation}&ip={ip_addr}"
    response2 = requests.get(url)
    data2 = response2.json()

    if response.status_code == 200:
        data = response.json()
        info = {
            'language':data2.get('language')
        }