# Import the dependencies.
import numpy as np
from scipy import stats

from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    #LIST ALL AVAILABLE ROUTES
    return(
        f"Available Routes:<br/>"
        "<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/yyyy-mm-dd<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    #QUERY PRECIPITATION ANALYSIS
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').order_by(Measurement.date).all()
    session.close()
    
    #CREATE DICTIONARY FOR DATA
    precipitation_list = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict[date] = prcp
        precipitation_list.append(precip_dict)

    #JSONIFY RESULTS
    return jsonify(precipitation_list)


@app.route("/api/v1.0/stations")
def stations():
    #QUERY LIST OF STATIONS
    #OPEN, QUERY, AND CLOSE SESSION
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()

    #CREATE LIST OF RESULTS - AS SEEN IN CLASS
    station_names = list(np.ravel(results))

    #JSONIFY LIST
    return jsonify(station_names)


@app.route("/api/v1.0/tobs")
def tobs():
    #QUERY DATES AND TEMP FOR MOST ACTIVE STATION OVER LAST YEAR
    #OPEN, QUERY, AND CLOSE SESSION
    session = Session(engine)
    results = session.query(Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').filter(Measurement.station == 'USC00519281').\
        order_by(Measurement.date).all()
    session.close()

    #CREATE LIST OF RESULTS
    most_active_tobs = list(np.ravel(results))

    #JSONIFY LIST
    return jsonify(most_active_tobs)


@app.route("/api/v1.0/<start>")
def start_only(start):
    #RETURN MIN, AVERAGE, MAX TEMP FOR SPECIFIED START
    #OPEN, QUERY, AND CLOSE SESSION
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()

    #CREATE LIST OF RESULTS
    min_avg_max = list(np.ravel(results))

    #JSONIFY LIST
    return jsonify(min_avg_max)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    #RETURN MIN, AVERAGE, MAX TEMP BETWEEN SPECIFIED START AND END
    #OPEN, QUERY, AND CLOSE SESSION
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    #CREATE LIST OF RESULTS
    start_end_math = list(np.ravel(results))

    #JSONIFY LIST
    return jsonify(start_end_math)


if __name__ == '__main__':
    app.run(debug=True)