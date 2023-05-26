# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

## Reminder: To run "app.py", go to containing folder, run GitBash from folder, enter envirnment, and use the command "python app.py" in GitBash

#################################################
# Database Setup
#################################################

# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)



#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#1 (all) = "/"
#________________________________________________
@app.route("/")
def welcome():
    return (f"Available Routes:<br/>"
    f"/api/v1.0/precipitation <br/>"
    f"/api/v1.0/stations <br/>"
    f"/api/v1.0/tobs <br/>"
    f"/api/v1.0/<start> <br/>"
    f"/api/v1.0/<start>/<end> <br/>")
    

#2 = "/api/v1.0/precipitation"
#________________________________________________
@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp_search = session.query(*[measurement.date, measurement.prcp]).\
        filter(measurement.date > (dt.date(2017, 8, 23) - dt.timedelta(days=365))).\
        order_by(measurement.date).all()

    prcp_results = []
    for date, prcp in prcp_search:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_results.append(prcp_dict)

    return jsonify(prcp_results)
       
#3 = "/api/v1.0/stations"
#________________________________________________
@app.route("/api/v1.0/stations")
def stations():
    stat_search = session.query(*[measurement.station]).\
        group_by(measurement.station).all()
    
    stat_result = list(np.ravel(stat_search))

    return jsonify(stat_result)

#4 = "/api/v1.0/tobs"
#________________________________________________
#4a Query last 12 months of temperature data from most-actice station
#4b Return Query as JSON response
@app.route("/api/v1.0/tobs")
def tobs():
    tobs_search = session.query(*[measurement.date,measurement.tobs]).\
        filter(measurement.date > (dt.date(2017, 8, 23) - dt.timedelta(days=365))).\
        filter(measurement.station == 'USC00519281').all()
    
    ##tobs_search
    tobs_results = []
    for date, tobs in tobs_search:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["prcp"] = tobs
        tobs_results.append(tobs_dict)

    return jsonify(tobs_results)

#5 = "/api/v1.0/<start>" and "/api/v1.0/<start>/<end>"
#________________________________________________
#5a Query based on variable date ranges that returns (for range): Min Temp, Max Temp, Avg Temp
    #5a1 Return Query as JSON response
#5b Query on specified start, calculate (for greater than date): "TMIN", "TMAX", "TAVG"
#5c Query based on variable date ranges that returns (for range)(inclusive): "TMIN", "TMAX", "TAVG"

#@app.route("/api/v1.0/<start>")
#def range_a(start):
    #range_a_search = start.replace(" ","").lower()
    #for date in measurment.date:
        #range_a_query = date

    #return jsonify({"error": f"Query for date {start} invalid."}), 404


if __name__ == '__main__':
    app.run(debug=True)