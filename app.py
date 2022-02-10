# Import all dependencies
import datetime as dt
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask setup
from flask import Flask, jsonify

app = Flask(__name__)

# Route to Homepage
@app.route("/")
def home():
    return (
        f"<h1>Wlecome to the Climate App Homepage<h1/>"
        f"<hr/>"
        f"<h2>All available API routes are shown below:<h2/>"
        f"<h3>Precipitation:<h3/><h5>/api/v1.0/precipitation<h5/>"
        f"<h3>Stations:<h3/><h5>/api/v1.0/stations<h5/>"
        f"<h3>Temperature Observations for the most active station:<h3/><h5>/api/v1.0/tobs<h5/>"
        f"<h3>Temperature Summary for the start date(yyyy-mm-dd):<h3/><h5>/api/v1.0/start<h5/>"
        f"<h3>Temperature Summary for the selected period:<h3/><h5>/api/v1.0/start_end<h5/>"
    )

# Route to precipiation
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    prcp = [Measurement.date, Measurement.prcp]
    prcp_query = session.query(*prcp).all()
    session.close()

    precipitation = []

    for date, prcp in prcp_query:
        prcp_json = {}
        prcp_json["Date"] = date
        prcp_json["Precipitation"] = prcp
        precipitation.append(prcp_json)

    return jsonify(precipitation)

# Route to stations
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    sel = [Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation]
    station_query = session.query(*sel).all()
    session.close()

    stations = []

    for station,name,lat,lon,el in station_query:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Lat"] = lat
        station_dict["Lon"] = lon
        station_dict["Elevation"] = el
        stations.append(station_dict)

    return jsonify(stations)
  
# Route to List of Temperature Observations for most active station
@app.route("/api/v1.0/tobs")
def temperature():
    session = Session(engine)
    start = '2016-08-23'
    sel =[Measurement.date, Measurement.tobs]
    active_station = 'USC00519281'
    query_tobs = session.query(*sel).\
                    filter(Measurement.date >= start, Measurement.station == active_station).\
                    group_by(Measurement.date).\
                    order_by(Measurement.date).all()
    session.close()

    tobs_station = []

    for date, tobs in query_tobs:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        tobs_station.append(tobs_dict)

    return jsonify(tobs_station)

# Route for TOBS for given Start Date
@app.route("/api/v1.0/start")
def start_date():
    session = Session(engine)
    start = '2016-08-23'
    start_result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()

    tobs_json = []
    for min,avg,max in start_result:
        tobs_dict = {}
        tobs_dict["Minimum Temperature"] = min
        tobs_dict["Average Temperature"] = avg
        tobs_dict["Maximum Temperature"] = max
        tobs_json.append(tobs_dict)

    return jsonify(tobs_json)

# Route for TOBS for given start and end range
@app.route("/api/v1.0/start_end")
def get_t_start_stop():
    session = Session(engine)
    start = '2016-08-23'
    end = '2017-08-23'
    query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    tobs_json = []
    for min,avg,max in query:
        tobs_dict = {}
        tobs_dict["Minimum Temperature"] = min
        tobs_dict["Average Temperature"] = avg
        tobs_dict["Maximum Temperature"] = max
        tobs_json.append(tobs_dict)

    return jsonify(tobs_json)

if __name__ == "__main__":
    app.run(debug=True)