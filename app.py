import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return (f"These are the available routes:<br/>"
            f"-------------------------------<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/start<br/>"
            f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #return "Precipitation Home"
    session = Session(engine)
    start_date='08-23-2016' 
    precip = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= start_date).all()
    #print(precip)
    session.close()
    precip_return = {"prcp": precip}

    return jsonify(precip_return)
    
@app.route("/api/v1.0/stations")
def stations():
    #return "Stations Home"
   session = Session(engine)
   stations = session.query(measurement.station).\
       group_by(measurement.station).all()
   session.close()
   station_return = {"Stations": stations}

   return jsonify(station_return)
    
@app.route("/api/v1.0/tobs")
def tobs():
   #return "TOBS Home"
   session = Session(engine)
   start_date='08-23-2016' 
   precip = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= start_date).\
        filter(measurement.station=='USC00519281').all()
   #print(precip)
   session.close()
   precip_return = {"prcp": precip}

   return jsonify(precip_return)
    
@app.route("/api/v1.0/start")
def start():
   min_temp = session.query(func.min(measurement.tobs)).\
       filter(measurement.station=='USC00519281').all()
   max_temp = session.query(func.max(measurement.tobs)).\
       filter(measurement.station=='USC00519281').all()
   avg_temp = session.query(func.avg(measurement.tobs)).\
       filter(measurement.station=='USC00519281').all()

   results = {"MinTemp": min_temp, "MaxTemp": max_temp, "AvgTemp": avg_temp}
   session.close()

   return jsonify(results)

@app.route("/api/v1.0/start/end")
def end():
    return "End Home"
    

if __name__ == "__main__":
    app.run(debug=True)
