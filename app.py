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
    conn = engine.connect()
    sql = "SELECT date, prcp FROM measurement WHERE date > '2016-08-23'"

    # Save the query results as a Pandas DataFrame and set the index to the date column
    # Sort the dataframe by date
    rain = pd.read_sql(sql, conn)
    rain.sort_values(by=['date'], ascending=True)
    rain.fillna(0, inplace=True)
    rain.set_index('date')
    rain = rain.to_json()
    return jsonify(rain)




@app.route("/api/v1.0/stations")
def stations():
    return "Stations Home"
    
@app.route("/api/v1.0/tobs")
def tobs():
    return "TOBS Home"
    
@app.route("/api/v1.0/start")
def start():
    return "Start Home"

@app.route("/api/v1.0/start/end")
def end():
    return "End Home"
    

if __name__ == "__main__":
    app.run(debug=True)
