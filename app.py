from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

import numpy as np
import pandas as pd

import datetime as dt
from datetime import timedelta


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(bind = engine)


app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"________________________<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/end" 
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    prcp_results = session.query(Measurement.date, Measurement.prcp).\
                filter(func.strftime("%Y-%m-%d", Measurement.date) >= dt.date(2016, 8, 23)).\
                filter(func.strftime("%Y-%m-%d", Measurement.date) <= dt.date(2017, 8, 23)).all()

    session.close()

    prec_list = []
    for date, prcp in prcp_results:
        prec_dict = {}
        prec_dict["date"] = date
        prec_dict["prcp"] = prcp
        prec_list.append(prec_dict)
    return jsonify(prec_list)

@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    station_query = session.query(Station.station, func.count(Measurement.station)).\
                join(Station, Station.station == Measurement.station).\
                group_by(Station.station).\
                order_by(func.count(Measurement.station).desc()).all()
    session.close()

    station_list = []
    for station, station_count in station_query:
        station_dict = {}
        station_dict["station"] = station
        station_dict["station_count"] = station_count
        station_list.append(station_dict)
    return jsonify(station_list)


    
    

@app.route("/api/v1.0/tobs")
def Tobs():
    session = Session(engine)
    most_active_station = "USC00519281"
    active_station_observation = session.query(Measurement.date, Measurement.tobs).\
                                filter_by(station = most_active_station).\
                                filter(func.strftime("%Y-%m-%d", Measurement.date) >= dt.date(2016, 8, 23)).all()

    session.close()

    tobs_list = []
    for date, tobs in active_station_observation:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)
    
    
# @app.route("/api/v1.0/<start_date>")
# def trip(start_date):
#     normals = []
#     trip_dates = []
#     delta = end_date - start_date 

#     for i in range(delta.days + 1):
#     day = start_date + timedelta(days=i)
#     trip_dates.append(day)

#     trip_month_day = [day.strftime("%m-%d") for day in trip_dates]

#     for date in trip_month_day:
#     daily_normal = daily_normals(date)
#     normals.append(daily_normal)

#     tmin = []
#     tavg = []
#     tmax = []
#     for normal in normals:
#         tmin.append(normal[0][0])
#         tavg.append(normal[0][1])
#         tmax.append(normal[0][2])

#     return 


if __name__ == "__main__":
    app.run(debug = True)