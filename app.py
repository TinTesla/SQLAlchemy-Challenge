# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt
from datetime import datetime

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

#5 = "/api/v1.0/<start>" 
#________________________________________________

@app.route("/api/v1.0/<start>")
        
def query_a(start):
    try:
        user_start = datetime.strptime(start, "%Y%m%d").date()
        results = session.query(func.min(measurement.tobs).label('tmin'),
                                func.max(measurement.tobs).label('tmax'),
                                func.avg(measurement.tobs).label('tavg')).\
                                filter(measurement.date > user_start).all()
        
        start_results = [] 
        
        for row in results:
            start_results.append((row.tmin, row.tmax, row.tavg))
            return jsonify(start_results)
        
    except Exception:
        error_message = f"An error occorred on query: {start}." 
        error_message += "\nPlease enter the date in the format 'YYYYMMDD'."
        error_message += "\nValid range is from 2010-1-1 to 2017-08-23."
        error_message += "\nIf date is valid: try refreshing your web browser, or restart the app and try again."
        return f"<pre>{error_message}</pre>"

#6 = "/api/v1.0/<start>/<end>" 
#________________________________________________

@app.route("/api/v1.0/<start>/<end>")
        
def query_b(start, end):
    try:
        user_start = datetime.strptime(start, "%Y%m%d").date()
        user_end = datetime.strptime(end, "%Y%m%d").date()
        results = session.query(func.min(measurement.tobs).label('tmin'),
                                func.max(measurement.tobs).label('tmax'),
                                func.avg(measurement.tobs).label('tavg')).\
                                filter(measurement.date < user_end).\
                                filter(measurement.date > user_start).all()
        
        start_results = [] 
        
        for row in results:
            start_results.append((row.tmin, row.tmax, row.tavg))
            return jsonify(start_results)
             
    except Exception:
        error_message = f"An error occorred on query: {start}/{end}." 
        error_message += "\nPlease enter the date in the format YYYYMMDD/YYYYMMDD."
        error_message += "\nValid range is from 2010-1-1 to 2017-08-23."
        error_message += "\nIf date is valid: try refreshing your web browser, or restart the app and try again."
        return f"<pre>{error_message}</pre>"


#End
#________________________________________________

if __name__ == '__main__':
    app.run(debug=True)