# Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np

from flask import Flask, jsonify

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)
# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)
# We can view all of the classes that automap found
Base.classes.keys()
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to my 'Home' page!"


# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation")
def hawaii_prcp():
    yr_prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= dt.date(2016, 8, 23)).order_by(Measurement.date)
    precipitation = {
        date: precipitation for date, precipitation in yr_prcp
    }

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def hawai_stations():
    stns = session.query(Station.station).all()
    stns = list(np.ravel(stns))
    return jsonify(stns)

@app.route("/api/v1.0/tobs")
def hawai_tobs():
    start_date = dt.date(2016, 8, 23)
    end_date = dt.date(2017, 8, 23)
    tobs = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    return jsonify(tobs)


if __name__ == "__main__":
    app.run(debug=True)
