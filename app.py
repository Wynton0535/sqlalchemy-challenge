# Import the dependencies.
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()

# reflect the tables

Base.prepare(engine, reflect= True)

# Save references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes"""
    return (
        f"Available routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"List of Stations: /api/v1.0/stations<br/>"
        f"Temperature for 1 year: /api/v1.0/tobs<br/>"
        f"Temperature from the start date: /api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"Temperature from the start to end dates: /api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create our session (link) from Python to the DB

    session = Session(engine)

    """Return a list of the Precipitation data"""
    # Query all Precipitation

    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-24").\
        all()
    session.close()

    # Convert the list to dictionary
    prec_all = []
    for date, prcp in results:
        prec_dict = {}
        prec_dict["date"] = date
        prec_dict["prcp"] = prcp

        prec_all.append(prec_dict)
    return jsonify(prec_all)
    
@app.route("/api/v1.0/stations")
def stations():

    # Create our session (link) from Python to the DB

    session = Session(engine)

    """Return a list of Stations data"""
    # Query all stations

    results = session.query(Station.station).\
        order_by(Station.station).all()
    session.close()

    # Convert list to tuples into normal list

    stations_all = list(np.ravel(results))

    return jsonify(stations_all)

@app.route("/api/v1.0/tobs")
def tobs():

    # Create our session (link) from Python to the DB

    session = Session(engine)

    """Return a list of al Temperatures for 1 year"""
    # Query all TOBs

    results = session.query(Measurement.date, Measurement.tobs, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-23").\
        filter(Measurement.station=='USC00519281').\
        order_by(Measurement.date).all()
    session.close()

    # Convert the list to dictionary

    tobs_all = []
    for prcp, date, tobs in results: 
        tobs_dict = {}
        tobs_dict["prcp"] = prcp
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs

        tobs_all.append(tobs_dict)
   
    return jsonify(tobs_all)

@app.route("/api/v1.0/<start_date>")
def Start_date(start_date):

    # Create our session (link) from Python to the DB

    session = Session(engine)

    """Return a list of min, avg, and max tobs for a start date"""

    # Query all TOBs

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    session.close()

    # Create a dictionary from the row data and append to a list of start_date_tobs

    start_date_tobs = []
    for min, avg, max in results: 
        start_date_tobs_dict = {}
        start_date_tobs_dict["min_temp"] = min
        start_date_tobs_dict["avg_temp"] = avg
        start_date_tobs_dict["max_temp"] = max
        start_date_tobs.append(start_date_tobs_dict)
    return jsonify(start_date_tobs)

@app.route("/api/v1.0/<start_date>/<end_date>")
def Start_end_date(start_date, end_date):

    # Create our session (link) from Python to the DB

    session = Session(engine)

    """Return a list of min, avg and max tobs for start and end dates"""
    
    # Query all tobs

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()
  
    # Create a dictionary from the row data and append to a list of start_end_date_tobs

    start_end_tobs = []
    for min, avg, max in results:
        start_end_tobs_dict = {}
        start_end_tobs_dict["min_temp"] = min
        start_end_tobs_dict["avg_temp"] = avg
        start_end_tobs_dict["max_temp"] = max
        start_end_tobs.append(start_end_tobs_dict) 
    

    return jsonify(start_end_tobs)

if __name__ == "__main__":
    app.run(debug=True)