import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#database set-up
engine = create_engine("sqlite:///hawaii.sqlite")

#reflect an existing database into a new model
Base = automap_base()
#reflect the tables
Base.prepare(engine, reflect=True)
#save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station
#Create our session (link) from Python to the DB
session = Session(engine)

#start and end dates for api starts/ends below
Start_Date = '2017-08-11'
End = '2017-08-21'

#Flask Set-Up
app = Flask(__name__)

#Flask Routes
@app.route("/")
def welcome():

    return (
        f"This is the Home Page: All available api routes are listed below:"
        f" Available Routes:<br/>"
        f"/api/stations<br/>"
        f"/api/precipitation<br/>"
        f"/api/temperature<br/>"
        f"/api/start<br/>"
        f"api/<start>/<end>"

    )
@app.route("/api/precipitation")
def precipitation():
    precipitation=session.query(Measurement.date, Measurement.prcp)
    precipitation_dict ={}
    for date in list(precipitation):
        precipitation_dict[date[0]] = date[1]
    return jsonify(precipitation_dict)

@app.route("/api/stations")
def stations():
    stations=session.query(Station.station)
    return jsonify(stations)

@app.route("/api/temperature")
def temperature():
    temperature = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= "2016-08-23").\
    filter(Measurement.date <=  "2017-08-23")
    return jsonify(temperature)

@app.route("/api/start")
def start_full():
    data = session.query(func.min(Measurement.tobs),
    func.max(Measurement.tobs),
    func.avg(Measurement.tobs)).\
    filter(Measurement.date >= "2017-08-11")
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

