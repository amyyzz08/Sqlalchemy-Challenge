# Import all dependencies
import datetime as dt
import numpy as np

# Database setup
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
        f"Precipitation:/precipitation<br/>"
        f"Stations:/stations<br/>"
        f"Temperature Observations:/tobs<br/>"
        f"Temperature Summary for the start date(yyyy-mm-dd):/api/v1.0/<start><br/>"
        f"Temperature Summary for the selected period:/api/v1.0/<start>/<end><br/>"
    )

# Route to precipiation
@app.route("/precipitation")
def precipitation():
    session = Session(engine)
    prec = [Measurement.date, Measurement.prec]
    prec_query = session.query(*sel).all()
    session.close()

    precipitation = []

    for date, prec in prec_query:
        prec_json = {}
        prec_json["Date"] = date
        prec_json["Precipitation"] = prec
        precipitation.append(prec_json)

    return jsonify(precipitation)

# Route to stations
@app.route("/stations")
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
  

# Route to List of Temperature Observations
@app.route("/tobs")
def temperature():
     session = Session(engine)
     active_station = session.query(Measurement.date, Measurement.tobs).\
                        filter(Measurement.date >= '2016-08-23').\
                        filter(Measurement.date <= '2017-08-23').\
                        filter(Measurement.station == 'USC00519281').all()
    sel = [Measurement.date, Measurement.tobs]
    station_query = session.query(*sel).filter(Measurement.station == 'USC00519281')
    session.close()

    tobs_json = []

    for date, tobs in station_query:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        tobs_json.append(tobs_dict)

    return jsonify(tobs_json)

if __name__ == "__main__":
    app.run(debug=True)