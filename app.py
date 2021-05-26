import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

######################################################
#  Database Set UP
######################################################

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect = True)

# Save references to each table
Measurement = Base.classes.measurement


######################################################
#  Flask Setup & Routes
######################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Available Routes:</br>"
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"</br>"
        f"Using 2017-08-23 as most recent date and 2010-01-01 as earliest date, let us search lowest, highest, and average temperature for station USC00519281 </br>"
        f"/api/v1.0/instert_start_date</br>"
        f"/api/v1.0/instert_start_date/instert_end_date</br>"
    )
        

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session
    session = Session(engine)

    # Session Query
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date.desc()).all()
    
    # Close session
    session.close()
    
    # Create a dictionary from the row data and append to a list of date and precipitation
    prcpt = []
    for date, prcp in results:
        prcpt_dict = {}
        prcpt_dict["date"] = date
        prcpt_dict["prcp"] = prcp
        prcpt.append(prcpt_dict)

    return jsonify(prcpt)
        

@app.route("/api/v1.0/stations")
def station():
    # Create our session
    session = Session(engine)
    
    # Session Query
    unique_station = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    
    # closing session
    session.close()
    
    station_name = list(np.ravel(unique_station))

    return jsonify(station_name)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session
    session = Session(engine)
    
    # Session Query
    station_of_interest = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23').filter(Measurement.station == 'USC00519281').all()
    
    #closing session
    session.close()
    
    
    # Create a dictionary for teperature and dates
    temp = []
    for date, tobs in station_of_interest:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["temperature_Of_Obs"] = tobs
        temp.append(temp_dict)

    return jsonify(temp)
    
    
@app.route("/api/v1.0/<start>")
def start_temp(start):
    
    # Create our session
    session = Session(engine)
    
    # Session Query
    start_temp = session.query(Measurement.station, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= start).all()
    
    #close session
    session.close()
    
    # Create a dictionary for teperature and dates
    select_temp = []
    for station, min_temp, max_temp, avg_temp in start_temp:
        select_temp_dict = {}
        select_temp_dict["min_temperature"] = min_temp
        select_temp_dict["max_temperature"] = max_temp
        select_temp_dict["average_temperature"] = round(avg_temp,2)
        select_temp.append(select_temp_dict)

    return jsonify(select_temp)


@app.route("/api/v1.0/<start>/<end>")
def start_end_temp(start, end):
    
    # Create our session
    session = Session(engine)
    
    # Session Query
    strt_end_temp = session.query(Measurement.station, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    
    #close session
    session.close()
    
    # Create a dictionary for teperature and dates
    interval_temp = []
    for station, min_temp, max_temp, avg_temp in strt_end_temp:
        interval_temp_dict = {}
        interval_temp_dict["min_temperature"] = min_temp
        interval_temp_dict["max_temperature"] = max_temp
        interval_temp_dict["average_temperature"] = round(avg_temp,2)
        interval_temp.append(interval_temp_dict)

    return jsonify(interval_temp)






if __name__ == '__main__':
    app.run(debug = True)