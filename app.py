from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

import pandas as pd

import datetime as dt
from datetime import timedelta, datetime


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
        f"To get precipitation data :<br/>"
        f"/api/v1.0/precipitation<br/><br/>"
        f"To get list of stations :<br/>"
        f"/api/v1.0/stations<br/><br/>"
        f"To get dates and temperature of the most active station for the last year :<br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"To get minimum, maximum and average temperature of all dates greater than and equal to the start date (date should be in yyyymmdd) :<br/>"
        f"/api/v1.0/&#60;start_date&#62;<br/><br/>"
        f"To get minimum, maximum and average temperature of dates between the start and end date inclusive (date should be in yyyymmdd) :<br/>"
        f"/api/v1.0/&#60;start_date&#62;/&#60;end_date&#62;<br/><br/>"
        f"__________________________<br/>"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
 
    """Fetch the 'date' as the key and 
    'prcp' as the value for our dataset.
    """

    session = Session(engine)
    prcp_results = session.query(Measurement.date, Measurement.prcp).all()

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
    
    """Fetch the list of station in our dataset.
    """
    
    session = Session(engine)
    
    station_query = session.query(Station.station).all()
    
    session.close()

    station_list = []
    for station in station_query:
        station_dict = {}
        station_dict["station"] = station
        station_list.append(station_dict)
    return jsonify(station_list)



@app.route("/api/v1.0/tobs")
def Tobs():
    
    """Query the dates and temperature observations of the 
    most active station for the last year of data.
    """
    
    session = Session(engine)
    
    station = session.query(Station.station, func.count(Measurement.station)).\
                join(Station, Station.station == Measurement.station).\
                group_by(Station.station).\
                order_by(func.count(Measurement.station).desc()).all()
    
    most_active_station = station[0][0]
    
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
    

    
@app.route("/api/v1.0/<start_date>")
def trip(start_date):
    
    """calculate TMIN, TAVG, and TMAX for 
    all dates greater than and equal to the start date.
    """
   
    session = Session(bind = engine)
    start_date = datetime.strptime(str(start_date), "%Y%m%d").strftime("%Y-%m-%d")

    start_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()

    session.close()

    trip_start_list = []
    for tmin, tavg, tmax in start_query:
        trip_start_dict = {}
        trip_start_dict["TMIN"] = tmin
        trip_start_dict["TAVG"] = tavg
        trip_start_dict["TMAX"] = tmax
        trip_start_list.append(trip_start_dict)
    return jsonify(trip_start_list)
    


@app.route("/api/v1.0/<start_date>/<end_date>")
def trip_startEnd(start_date, end_date):
    
    """ calculate the TMIN, TAVG, and TMAX for 
    dates between the start and end date inclusive."""
    
    session = Session(bind = engine)
    start_date = datetime.strptime(str(start_date), "%Y%m%d").strftime("%Y-%m-%d")
    end_date = datetime.strptime(str(end_date), "%Y%m%d").strftime("%Y-%m-%d")

    startEnd_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    trip_startEnd_list = []
    for tmin, tavg, tmax in startEnd_query:
        trip_startEnd_dict = {}
        trip_startEnd_dict["TMIN"] = tmin
        trip_startEnd_dict["TAVG"] = tavg
        trip_startEnd_dict["TMAX"] = tmax
        trip_startEnd_list.append(trip_startEnd_dict)
    return jsonify(trip_startEnd_list)



if __name__ == "__main__":
    app.run(debug = True)