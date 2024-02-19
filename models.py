import requests
from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from flask_sqlalchemy import SQLAlchemy

from app import db

class WeatherData(db.Model):
    id = Column(Integer, primary_key=True)
    city = Column(String(80), nullable=False)
    description = Column(String(120))
    temperature = Column(Float)