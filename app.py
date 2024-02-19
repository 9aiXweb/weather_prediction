# import requests
# from flask import Flask, render_template, request

# app = Flask(__name__)

# API_KEY = "cb244b3767f2404bfebbbeaa1c3f7d4e"  

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         city = request.form['city']
#         url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
#         data = requests.get(url).json()

#         # Extract weather info if the API call is successful, else error
#         if data['cod'] == '404':
#             return render_template('index.html')
#         else:
#             weather = data['weather'][0]['description']
#             temp = data['main']['temp']

#         return render_template('index.html', city=city, weather=weather, temp=temp)

#     else:
#         return render_template('index.html')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0') 

import requests
from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from flask_sqlalchemy import SQLAlchemy

# Database config 
DB_URI = 'sqlite:///weather_data.db'  # Using SQLite (adjust for other DBs)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
db = SQLAlchemy(app)

# Weather data model
class WeatherData(db.Model):
    id = Column(Integer, primary_key=True)
    city = Column(String(80), nullable=False)
    description = Column(String(120))
    temperature = Column(Float)

# Create database tables (Run once initially to set up DB)
db.create_all() 

API_KEY = "cb244b3767f2404bfebbbeaa1c3f7d4e"  

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()

        # Extract weather info if the API call is successful, else error
        if data['cod'] == '404':
            return render_template('index.html')
        else:
            weather = data['weather'][0]['description']
            temp = data['main']['temp']

        return render_template('index.html', city=city, weather=weather, temp=temp)

    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0') 

