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
    prcp_results = session.query(Measurement.date, Measurement.prcp).\
                filter(func.strftime("%Y-%m-%d", Measurement.date) >= dt.date(2016, 8, 23)).\
                filter(func.strftime("%Y-%m-%d", Measurement.date) <= dt.date(2017, 8, 23)).all()

    prec_dict = {}
    for result in prcp_results:
        prec_dict["Date"] = result[0][0],
        prec_dict["Precipitation"] = result[0][1]})
    
    return jsonify(prcp_dict)




if __name__ == "__main__":
    app.run(debug = True)