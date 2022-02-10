# Import all dependencies
import datetime as dt
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")
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
    print("Wlecome to the Climate App Homepage")
    print("All available API routes are shown below:")
    return (
        f"Precipitation:/api/v1.0/precipitation<br/>"
        f"Stations:/api/v1.0/stations<br/>"
        f"Temperature Observations for the most active station:/api/v1.0/tobs<br/>"
        f"Temperature Summary for the start date(yyyy-mm-dd):/api/v1.0/<start><br/>"
        f"Temperature Summary for the selected period:/api/v1.0/<start>/<end><br/>"
    )

# Route to precipiation
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    prec = [Measurement.date, Measurement.prec]
    prec_query = session.query(*prec).all()
    session.close()

    precipitation = []

    for date, prec in prec_query:
        prec_json = {}
        prec_json["Date"] = date
        prec_json["Precipitation"] = prec
        precipitation.append(prec_json)

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
# @app.route("/api/v1.0/tobs")
# def temperature():
#      session = Session(engine)
#      start = '2016-08-23'
#      sel =[Measurement.date, Measurement.tobs]
#      active_station = 'USC00519281'
#      station_tobs = session.query(*sel).\
#                     filter(Measurement.date >= start, Measurement.station == active_station).\
#                     group_by(Measurement.date).\
#                     order_by(Measurement.date).all()
#     session.close()


# Route for TOBS for given Start Date
@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
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
@app.route("/api/v1.0/<start>/<end>")
def get_t_start_stop(start,end):
    session = Session(engine)
    query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    tobs_json = []
    for min,avg,max in query:
        tobs_dict = {}
        tobs_dict["Minimum Temperature"] = min
        tobs_dict["Average Temperature"] = avg
        tobs_dict["aximum Temperature"] = max
        tobs_json.append(tobs_dict)

    return jsonify(tobs_json)

if __name__ == "__main__":
    app.run(debug=True)