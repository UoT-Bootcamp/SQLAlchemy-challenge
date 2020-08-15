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
    station_query = session.query(Station.station, func.count(Measurement.station)).\
                join(Station, Station.station == Measurement.station).\
                group_by(Station.station).\
                order_by(func.count(Measurement.station).desc()).all()
    return jsonify(station_query)
    

@app.route("/api/v1.0/tobs")
def Tobs():
    most_active_station = "USC00519281"
    active_station_observation = session.query(Measurement.date, Measurement.tobs).\
                                filter_by(station = most_active_station).\
                                filter(func.strftime("%Y-%m-%d", Measurement.date) >= dt.date(2016, 8, 23)).all()
                                
    return jsonify(active_station_observation)


if __name__ == "__main__":
    app.run(debug = True)