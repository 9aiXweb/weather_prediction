import requests
from flask import Flask, render_template

app = Flask(__name__)

API_KEY = "cb244b3767f2404bfebbbeaa1c3f7d4e"  

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()

        # Extract weather info if the API call is successful, else error
        if data['cod'] == '404':
            error = 'City not found!'
        else:
            weather = data['weather'][0]['description']
            temp = data['main']['temp']

        return render_template('index.html', city=city, weather=weather, temp=temp, error=error)

    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0') 
