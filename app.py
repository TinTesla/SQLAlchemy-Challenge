# Import the dependencies.
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
measurment = Base.classes.measurement
station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#Hints
#________________________________________________
#A = Join "Station" and "Measurement" tables
#B = use "Jsonify" to convert API Query to JSON response


#1 (all) = "/"
#________________________________________________
#1a Homepage
#1b Return All possible Paths


#2 = "/api/v1.0/precipitation"
#________________________________________________
#2a Convay query for last 12 months of precipitation data
#2b Return query as JSON response


#3 = "/api/v1.0/stations"
#________________________________________________
#3 Return query of all Sations as JSON response


#4 = "/api/v1.0/tobs"
#________________________________________________
#4a Query last 12 months of temperature data from most-actice station
#4b Return Query as JSON response


#5 = "/api/v1.0/<start>" and "/api/v1.0/<start>/<end>"
#________________________________________________
#5a Query based on variable date ranges that returns (for range): Min Temp, Max Temp, Avg Temp
    #5a1 Return Query as JSON response
#5b Query on specified start, calculate (for greater than date): "TMIN", "TMAX", "TAVG"
#5c Query based on variable date ranges that returns (for range)(inclusive): "TMIN", "TMAX", "TAVG"
