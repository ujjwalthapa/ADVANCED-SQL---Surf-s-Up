
# Surf's Up!  Assignment
## Includes: Flask/API code from Hawaii_app.py and db_prepare.py (SQLalchemy boilerplate)
###   -produced by Verna Orsatti August 5, 2018




```python
%matplotlib notebook
from matplotlib import style
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('fivethirtyeight') 
```


```python
import numpy as np
import pandas as pd
```


```python
import datetime as dt
from datetime import datetime
```

# Reflect Tables into SQLAlchemy ORM


```python
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect
```


```python
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
```


```python
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
```


```python
# We can view all of the classes that automap found
Base.classes.keys()
```




    ['measurement', 'station']




```python
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
```


```python
# Create our session (link) from Python to the DB
session = Session(engine)
```


```python
inspector = inspect(engine)
inspector
```




    <sqlalchemy.engine.reflection.Inspector at 0x112a9c400>




```python
# Rename Base to schema
schema = Base
schema.classes.items()
```




    [('measurement', sqlalchemy.ext.automap.measurement),
     ('station', sqlalchemy.ext.automap.station)]




```python
# Use inspector to view table details
for table_name in inspector.get_table_names():
    for column in inspector.get_columns(table_name):
        print( table_name,": ", column.get('name'), ", ", column.get('type'))
```

    measurement :  id ,  INTEGER
    measurement :  station ,  TEXT
    measurement :  date ,  TEXT
    measurement :  prcp ,  FLOAT
    measurement :  tobs ,  FLOAT
    station :  id ,  INTEGER
    station :  station ,  TEXT
    station :  name ,  TEXT
    station :  latitude ,  FLOAT
    station :  longitude ,  FLOAT
    station :  elevation ,  FLOAT


## Sharing the Aiden Health Tracker
- Run locally: `python aiden_health_app.py` (defaults to `http://127.0.0.1:5000`) and copy the dashboard's "Share the tracker" link for others.
- Let others on your network view it: `AIDEN_HOST=0.0.0.0 python aiden_health_app.py` and share `http://<your-local-ip>:5000/`.
- Change the port if needed: `AIDEN_PORT=8080 python aiden_health_app.py` then share `http://<your-local-ip>:8080/`.
- For internet sharing, deploy to a hosting service (e.g., render.com, Railway, Fly.io) and use the provided public URL; avoid exposing your home IP directly.


# Precipitation Analysis


```python
# Design a query to retrieve the last 12 months of precipitation 
# data and plot the results
# There are multiple stations per date: Yes
```


```python
# Calculate the date 1 year ago from today
most_recent_date = session.query(Measurement.date)\
    .order_by(Measurement.date.desc()).first()
most_recent_date 
```




    ('2017-08-23')




```python
# Reduce most recent date of data collected, reduced by 1 year for query for 365 days
rec_date = str(most_recent_date)[2:-3]
year_ago = str(eval(rec_date[0:4])-1) + rec_date[4:]
year_ago
```




    '2016-08-23'




```python
# View Test information from Measurement
# An average of the Station's precipitation measurment is used for this analysis as it made more analysis sense.
#   The original requirements were for querying precipitation amounts, without mention of average
test_precip_twelve = session.query(Measurement.date,
                                   func.avg(Measurement.prcp))\
    .filter(Measurement.date > year_ago)\
    .group_by(Measurement.date)\
    .order_by(Measurement.date).all()
    
for row in test_precip_twelve:
    print(row)
```

    ('2016-08-24', 1.5549999999999997)
    ('2016-08-25', 0.07714285714285715)
    ('2016-08-26', 0.016666666666666666)
    ('2016-08-27', 0.06399999999999999)
    ('2016-08-28', 0.5166666666666666)
    ('2016-08-29', 0.24333333333333332)
    ('2016-08-30', 0.011666666666666667)
    ('2016-08-31', 0.6359999999999999)
    ('2016-09-01', 0.006)
    ('2016-09-02', 0.05)
    ('2016-09-03', 0.254)
    ('2016-09-04', 0.276)
    ('2016-09-05', 0.08499999999999999)
    ('2016-09-06', 0.246)
    ('2016-09-07', 0.3333333333333333)
    ('2016-09-08', 0.07666666666666667)
    ('2016-09-09', 0.17833333333333332)
    ('2016-09-10', 0.27999999999999997)
    ('2016-09-11', 0.25)
    ('2016-09-12', 0.308)
    ('2016-09-13', 0.45166666666666666)
    ('2016-09-14', 2.3800000000000003)
    ('2016-09-15', 0.8266666666666667)
    ('2016-09-16', 0.11714285714285715)
    ('2016-09-17', 0.13599999999999998)
    ('2016-09-18', 0.10600000000000001)
    ('2016-09-19', 0.064)
    ('2016-09-20', 0.14714285714285716)
    ('2016-09-21', 0.19499999999999998)
    ('2016-09-22', 0.2057142857142857)
    ('2016-09-23', 0.22428571428571428)
    ('2016-09-24', 0.04666666666666667)
    ('2016-09-25', 0.015)
    ('2016-09-26', 0.2783333333333333)
    ('2016-09-27', 0.22666666666666666)
    ('2016-09-28', 0.018571428571428572)
    ('2016-09-29', 0.42714285714285716)
    ('2016-09-30', 0.19166666666666665)
    ('2016-10-01', 0.2416666666666667)
    ('2016-10-02', 0.12)
    ('2016-10-03', 0.115)
    ('2016-10-04', 0.5816666666666667)
    ('2016-10-05', 0.1366666666666667)
    ('2016-10-06', 0.022857142857142857)
    ('2016-10-07', 0.0016666666666666668)
    ('2016-10-08', 0.008)
    ('2016-10-09', 0.0)
    ('2016-10-10', 0.0)
    ('2016-10-11', 0.11499999999999999)
    ('2016-10-12', 0.013333333333333334)
    ('2016-10-13', 0.013333333333333334)
    ('2016-10-14', 0.0)
    ('2016-10-15', 0.065)
    ('2016-10-16', 0.0)
    ('2016-10-17', 0.11000000000000001)
    ('2016-10-18', 0.09999999999999999)
    ('2016-10-19', 0.028333333333333332)
    ('2016-10-20', 0.202)
    ('2016-10-21', 0.064)
    ('2016-10-22', 0.354)
    ('2016-10-23', 0.055999999999999994)
    ('2016-10-24', 0.13166666666666665)
    ('2016-10-25', 0.15714285714285717)
    ('2016-10-26', 0.04833333333333334)
    ('2016-10-27', 0.31)
    ('2016-10-28', 0.09500000000000001)
    ('2016-10-29', 0.10666666666666667)
    ('2016-10-30', 0.26499999999999996)
    ('2016-10-31', 0.26833333333333337)
    ('2016-11-01', 0.035)
    ('2016-11-02', 0.006666666666666667)
    ('2016-11-03', 0.0033333333333333335)
    ('2016-11-04', 0.01)
    ('2016-11-05', 0.075)
    ('2016-11-06', 0.013333333333333334)
    ('2016-11-07', 0.03)
    ('2016-11-08', 0.18666666666666668)
    ('2016-11-09', 0.05714285714285714)
    ('2016-11-10', 0.0016666666666666668)
    ('2016-11-11', 0.0)
    ('2016-11-12', 0.0)
    ('2016-11-13', 0.0)
    ('2016-11-14', 0.02142857142857143)
    ('2016-11-15', 0.008333333333333333)
    ('2016-11-16', 0.25666666666666665)
    ('2016-11-17', 0.01)
    ('2016-11-18', 0.0075)
    ('2016-11-19', 0.095)
    ('2016-11-20', 0.23750000000000002)
    ('2016-11-21', 0.616)
    ('2016-11-22', 1.002)
    ('2016-11-23', 0.134)
    ('2016-11-24', 0.296)
    ('2016-11-25', 0.264)
    ('2016-11-26', 0.085)
    ('2016-11-27', 0.09166666666666667)
    ('2016-11-28', 0.12)
    ('2016-11-29', 0.07166666666666667)
    ('2016-11-30', 0.17666666666666667)
    ('2016-12-01', 0.295)
    ('2016-12-02', 0.3933333333333333)
    ('2016-12-03', 0.45166666666666666)
    ('2016-12-04', 0.13333333333333333)
    ('2016-12-05', 0.54)
    ('2016-12-06', 0.008)
    ('2016-12-07', 0.076)
    ('2016-12-08', 0.06571428571428573)
    ('2016-12-09', 0.37)
    ('2016-12-10', 0.026000000000000002)
    ('2016-12-11', 0.05)
    ('2016-12-12', 0.008333333333333333)
    ('2016-12-13', 0.12833333333333333)
    ('2016-12-14', 0.25)
    ('2016-12-15', 0.043333333333333335)
    ('2016-12-16', 0.006666666666666667)
    ('2016-12-17', 0.07)
    ('2016-12-18', 0.178)
    ('2016-12-19', 0.07)
    ('2016-12-20', 0.005)
    ('2016-12-21', 0.1285714285714286)
    ('2016-12-22', 0.4116666666666666)
    ('2016-12-23', 0.205)
    ('2016-12-24', 0.27)
    ('2016-12-25', 0.086)
    ('2016-12-26', 0.40800000000000003)
    ('2016-12-27', 0.04)
    ('2016-12-28', 0.06833333333333334)
    ('2016-12-29', 0.39666666666666667)
    ('2016-12-30', 0.5583333333333333)
    ('2016-12-31', 0.42800000000000005)
    ('2017-01-01', 0.06999999999999999)
    ('2017-01-02', 0.004)
    ('2017-01-03', 0.0)
    ('2017-01-04', 0.03)
    ('2017-01-05', 0.15833333333333333)
    ('2017-01-06', 0.13333333333333333)
    ('2017-01-07', 0.01)
    ('2017-01-08', 0.01)
    ('2017-01-09', 0.0)
    ('2017-01-10', 0.0)
    ('2017-01-11', 0.0)
    ('2017-01-12', 0.0)
    ('2017-01-13', 0.0)
    ('2017-01-14', 0.002)
    ('2017-01-15', 0.0025)
    ('2017-01-16', 0.0)
    ('2017-01-17', 0.0)
    ('2017-01-18', 0.011666666666666667)
    ('2017-01-19', 0.0033333333333333335)
    ('2017-01-20', 0.0)
    ('2017-01-21', 0.04666666666666666)
    ('2017-01-22', 0.20400000000000001)
    ('2017-01-23', 0.188)
    ('2017-01-24', 0.45)
    ('2017-01-25', 0.716)
    ('2017-01-26', 0.015714285714285715)
    ('2017-01-27', 0.008571428571428572)
    ('2017-01-28', 0.028000000000000004)
    ('2017-01-29', 0.2475)
    ('2017-01-30', 0.008333333333333333)
    ('2017-01-31', 0.0)
    ('2017-02-01', 0.0)
    ('2017-02-02', 0.0)
    ('2017-02-03', 0.0)
    ('2017-02-04', 0.0)
    ('2017-02-05', 0.0)
    ('2017-02-06', 0.06333333333333334)
    ('2017-02-07', 1.0571428571428572)
    ('2017-02-08', 0.1542857142857143)
    ('2017-02-09', 0.002857142857142857)
    ('2017-02-10', 0.0)
    ('2017-02-11', 1.866666666666667)
    ('2017-02-12', 1.7466666666666668)
    ('2017-02-13', 0.4866666666666666)
    ('2017-02-14', 0.0016666666666666668)
    ('2017-02-15', 0.016)
    ('2017-02-16', 0.36999999999999994)
    ('2017-02-17', 0.17500000000000004)
    ('2017-02-18', 0.0025)
    ('2017-02-19', 0.0475)
    ('2017-02-20', 0.0)
    ('2017-02-21', 0.026000000000000002)
    ('2017-02-22', 0.13000000000000003)
    ('2017-02-23', 0.0014285714285714286)
    ('2017-02-24', 0.0)
    ('2017-02-25', 0.0375)
    ('2017-02-26', 0.0)
    ('2017-02-27', 0.0)
    ('2017-02-28', 0.13666666666666666)
    ('2017-03-01', 1.6600000000000001)
    ('2017-03-02', 1.0933333333333333)
    ('2017-03-03', 0.37166666666666665)
    ('2017-03-04', 0.0)
    ('2017-03-05', 0.3025)
    ('2017-03-06', 0.135)
    ('2017-03-07', 0.0)
    ('2017-03-08', 0.0)
    ('2017-03-09', 0.3266666666666667)
    ('2017-03-10', 0.04142857142857143)
    ('2017-03-11', 0.008)
    ('2017-03-12', 0.0)
    ('2017-03-13', 0.0)
    ('2017-03-14', 0.008571428571428572)
    ('2017-03-15', 0.01)
    ('2017-03-16', 0.0)
    ('2017-03-17', 0.144)
    ('2017-03-18', 0.0)
    ('2017-03-19', 0.0)
    ('2017-03-20', 0.004)
    ('2017-03-21', 0.015)
    ('2017-03-22', 0.0)
    ('2017-03-23', 0.008333333333333333)
    ('2017-03-24', 0.18833333333333335)
    ('2017-03-25', 0.394)
    ('2017-03-26', 0.0)
    ('2017-03-27', 0.002)
    ('2017-03-28', 0.11833333333333335)
    ('2017-03-29', 0.03166666666666667)
    ('2017-03-30', 0.03)
    ('2017-03-31', 0.0016666666666666668)
    ('2017-04-01', 0.06833333333333334)
    ('2017-04-02', 0.0)
    ('2017-04-03', 0.11)
    ('2017-04-04', 0.02142857142857143)
    ('2017-04-05', 0.09428571428571429)
    ('2017-04-06', 0.008571428571428572)
    ('2017-04-07', 0.0)
    ('2017-04-08', 0.0)
    ('2017-04-09', 0.0)
    ('2017-04-10', 0.0033333333333333335)
    ('2017-04-11', 0.07833333333333332)
    ('2017-04-12', 0.18000000000000002)
    ('2017-04-13', 0.18166666666666667)
    ('2017-04-14', 1.1199999999999999)
    ('2017-04-15', 0.34800000000000003)
    ('2017-04-16', 0.21400000000000002)
    ('2017-04-17', 0.6140000000000001)
    ('2017-04-18', 0.48)
    ('2017-04-19', 0.03333333333333333)
    ('2017-04-20', 0.13)
    ('2017-04-21', 1.3966666666666667)
    ('2017-04-22', 0.9920000000000002)
    ('2017-04-23', 0.11499999999999999)
    ('2017-04-24', 0.015000000000000001)
    ('2017-04-25', 0.0)
    ('2017-04-26', 0.065)
    ('2017-04-27', 0.06999999999999999)
    ('2017-04-28', 0.7066666666666667)
    ('2017-04-29', 1.3399999999999999)
    ('2017-04-30', 1.07)
    ('2017-05-01', 0.135)
    ('2017-05-02', 0.008333333333333333)
    ('2017-05-03', 0.006)
    ('2017-05-04', 0.016)
    ('2017-05-05', 0.06333333333333334)
    ('2017-05-06', 0.01)
    ('2017-05-07', 0.024)
    ('2017-05-08', 0.5016666666666666)
    ('2017-05-09', 0.9260000000000002)
    ('2017-05-10', 0.14333333333333334)
    ('2017-05-11', 0.12)
    ('2017-05-12', 0.032)
    ('2017-05-13', 0.048)
    ('2017-05-14', 0.244)
    ('2017-05-15', 0.176)
    ('2017-05-16', 0.06999999999999999)
    ('2017-05-17', 0.025000000000000005)
    ('2017-05-18', 0.14166666666666666)
    ('2017-05-19', 0.01)
    ('2017-05-20', 0.0075)
    ('2017-05-21', 0.002)
    ('2017-05-22', 0.072)
    ('2017-05-23', 0.11833333333333333)
    ('2017-05-24', 0.6483333333333333)
    ('2017-05-25', 0.37000000000000005)
    ('2017-05-26', 0.004)
    ('2017-05-27', 0.085)
    ('2017-05-28', 0.06833333333333334)
    ('2017-05-29', 0.084)
    ('2017-05-30', 0.346)
    ('2017-05-31', 0.074)
    ('2017-06-01', 0.006666666666666667)
    ('2017-06-02', 0.06799999999999999)
    ('2017-06-03', 0.122)
    ('2017-06-04', 0.19166666666666665)
    ('2017-06-05', 0.013333333333333334)
    ('2017-06-06', 0.0)
    ('2017-06-07', 0.0016666666666666668)
    ('2017-06-08', 0.005)
    ('2017-06-09', 0.008)
    ('2017-06-10', 0.306)
    ('2017-06-11', 0.35833333333333334)
    ('2017-06-12', 0.2916666666666667)
    ('2017-06-13', 0.22999999999999998)
    ('2017-06-14', 0.26166666666666666)
    ('2017-06-15', 0.45166666666666666)
    ('2017-06-16', 0.03333333333333333)
    ('2017-06-17', 0.09000000000000001)
    ('2017-06-18', 0.23666666666666666)
    ('2017-06-19', 0.12166666666666666)
    ('2017-06-20', 0.11000000000000001)
    ('2017-06-21', 0.1275)
    ('2017-06-22', 0.07333333333333335)
    ('2017-06-23', 0.11166666666666665)
    ('2017-06-24', 0.128)
    ('2017-06-25', 0.12)
    ('2017-06-26', 0.02)
    ('2017-06-27', 0.018333333333333333)
    ('2017-06-28', 0.005)
    ('2017-06-29', 0.011666666666666667)
    ('2017-06-30', 0.07428571428571429)
    ('2017-07-01', 0.065)
    ('2017-07-02', 0.18)
    ('2017-07-03', 0.148)
    ('2017-07-04', 0.037500000000000006)
    ('2017-07-05', 0.0)
    ('2017-07-06', 0.004)
    ('2017-07-07', 0.1)
    ('2017-07-08', 0.016666666666666666)
    ('2017-07-09', 0.03333333333333333)
    ('2017-07-10', 0.006666666666666667)
    ('2017-07-11', 0.005)
    ('2017-07-12', 0.060000000000000005)
    ('2017-07-13', 0.3016666666666667)
    ('2017-07-14', 0.15833333333333335)
    ('2017-07-15', 0.03166666666666667)
    ('2017-07-16', 0.135)
    ('2017-07-17', 0.15166666666666667)
    ('2017-07-18', 0.3614285714285714)
    ('2017-07-19', 0.06833333333333334)
    ('2017-07-20', 0.17714285714285713)
    ('2017-07-21', 0.018571428571428572)
    ('2017-07-22', 0.7366666666666667)
    ('2017-07-23', 0.22600000000000003)
    ('2017-07-24', 0.6539999999999999)
    ('2017-07-25', 0.08714285714285715)
    ('2017-07-26', 0.08333333333333333)
    ('2017-07-27', 0.0016666666666666668)
    ('2017-07-28', 0.11)
    ('2017-07-29', 0.10166666666666667)
    ('2017-07-30', 0.06)
    ('2017-07-31', 0.0)
    ('2017-08-01', 0.04666666666666666)
    ('2017-08-02', 0.075)
    ('2017-08-03', 0.017499999999999998)
    ('2017-08-04', 0.015)
    ('2017-08-05', 0.03)
    ('2017-08-06', 0.0)
    ('2017-08-07', 0.0125)
    ('2017-08-08', 0.11000000000000001)
    ('2017-08-09', 0.049999999999999996)
    ('2017-08-10', 0.0175)
    ('2017-08-11', 0.0)
    ('2017-08-12', 0.04666666666666667)
    ('2017-08-13', 0.0)
    ('2017-08-14', 0.062)
    ('2017-08-15', 0.164)
    ('2017-08-16', 0.1525)
    ('2017-08-17', 0.0475)
    ('2017-08-18', 0.02)
    ('2017-08-19', 0.03)
    ('2017-08-20', 0.005)
    ('2017-08-21', 0.19333333333333336)
    ('2017-08-22', 0.16666666666666666)
    ('2017-08-23', 0.1325)



```python
# Create dataframe in the rough and sort by date for graph
precip_df = pd.DataFrame(test_precip_twelve, columns=['date','prcp'])
precip_df['date'] = pd.to_datetime(precip_df['date'], format='%Y/%m/%d')
precip_df.sort_values(by=['date'])
precip_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>prcp</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2016-08-24</td>
      <td>1.555000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2016-08-25</td>
      <td>0.077143</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2016-08-26</td>
      <td>0.016667</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2016-08-27</td>
      <td>0.064000</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2016-08-28</td>
      <td>0.516667</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Reset index to Date and drop dates with no measurements taken for precipitation.
# This Dataframe is just for the graff of precipation amounts recorded.  
precip_df.set_index('date', inplace=True)
precip_df.dropna(inplace=True)
precip_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>prcp</th>
    </tr>
    <tr>
      <th>date</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2016-08-24</th>
      <td>1.555000</td>
    </tr>
    <tr>
      <th>2016-08-25</th>
      <td>0.077143</td>
    </tr>
    <tr>
      <th>2016-08-26</th>
      <td>0.016667</td>
    </tr>
    <tr>
      <th>2016-08-27</th>
      <td>0.064000</td>
    </tr>
    <tr>
      <th>2016-08-28</th>
      <td>0.516667</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Use Pandas Plotting with Matplotlib to plot the data
precip_df.plot(use_index=True, y='prcp', figsize=(8,5))
plt.gcf().subplots_adjust(bottom=0.15)
plt.title("Hawaii Precipitation Measurements \n Stations Combined - Averaged by Date", fontweight='bold',size=10)
plt.xlabel(f"Date Range:  {year_ago} - {rec_date}", fontweight='bold', size=9)
plt.ylabel("Precipitation (inches)", fontweight='bold', size=9)
plt.yticks(size=7)
plt.xticks(rotation=45, size=7)
plt.legend(["precipitation"],loc=1, fontsize='small', bbox_to_anchor=(.90, 1))
plt.tight_layout()
plt.savefig('precipitation_amounts.png')
plt.show()
```


    <IPython.core.display.Javascript object>



<img src="data:image/png;base64,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eMQj9JKXvESPetSj1injIQ95iK6//vqm5da3grTb+nHdddfp/e9/v376059q4cKFmj59uh7+8IfLdT7ooIPuV/aTnvQk/fznPx/qK/eDt538+te/1sqVK4f6xH3d7Lp2VoVQMfwx1+6KQus9QkXebstTGkIFQkUfTA55jLmHpRSaRHvYwu5uDZ84P1jFWMEJBzxmKXDqRqhYsHSVblq6arioe5J/7pSJmjclz9bZ5Ag/73nP0+c+97mhgyQ322wz/epXvxraBmGB4Nxzz9UDHvCA+9qaHHoLB3Zy7TD7ug022EBbb7213vnOdw7lvfDCC3XiiSdqyZIlQ1szdtxxxyEH/re//a18vsMrXvEKvfnNb16H4W233aanPOUpuuKKKzR16tQhB3+TTTYZqsvVV1895Eh/9atfDQsVrdo1b948/ehHP2rarvphml/60pf0ne98Z0homT17tg455JD77m0BxyKEhQr//8tf/rJ23nlnbbnllkO/+9vf/qZrrrlGEydO1Kc//emhdqVkocR8fv/732vXXXeVhYuULCgcdthhQz+2Eip++ctf6phjjtHixYuH2Pp6C0GXXXaZ1qxZo7e85S16+ctfvg7bJFS89KUv1cc//vGh+7oNf/rTn4YEIdfTwsv+++8ftmuEijCqUMZC6z1CRag3CmdCqOgvoeL0gzfV4Wz9KDwKur9doUm0+4r2qAT4xMHDKsYKTjjgMUuBUzdCRaco0OH2wWjmf83u0/W6h22c5RbJEXYExdlnnz30Rt5pxYoVes5znjPkpFscsAObUhIq/LPFijPPPHMoeqCe7DQ74sDnPthJP+qoo+77s89dsNPuiAKXX4+QsPN9/vnn68ADDxwSTiyapOQve9ix33fffe/7XaeIimbtev7zn69vf/vbLdvV+NWPyNaPSy65RNtss82QSFFP5513no4//vgh0cViwJQpU+7780gP07TIY+4WCRx94UiICRMmDJVr8eO4444b6j8LMXvttdd990tChfM6eiYJJxY2Xv3qV+szn/nMENvvf//7YdtCqAijCmUstN4jVIR6o3AmhIqyQsV7L1+s97bZ+oFQUXgAZLpdoUk0U23LFwOfOHNYxVjBaS0nWGAzMQLr5mp0ppp9rWG8CxV+++638PXkKAZvXbj77rvlN/iOiHCqCxWONLDT3Jje9KY36aMf/ejQ1yzs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QyVdX1aQvm8TMIGWCbjiQMsIfQATMAETyE/AQkV+Vt7SBEzABEyg/QSqhQ3xM2LGfy6JpJuxUcaU5KRUCaGcYGzTJc1r/6X7jCZgAiZgAiZgAiZgAs0QsFDRDDXvYwImYAImsC4JENJBRaLtQ3WLGxMXs3MozbmfpL+HmHKvhK7Lp+Vzm4AJmIAJmIAJmECDBCxUNAjMm5uACZiACawTAluGEsmUFV0s6YWSzpR0naRvJkJAuDgSan4o9bN1ctE+qQmYgAmYgAmYgAmYQOMELFQ0zsx7mIAJmIAJtJcAiTO3kzRR0gOSTgxlk/GaOCOEgVwk6VxJ75D0UUmUxe32EqTtfQo+mwmYgAmYgAmYgAm0iYCFijaB9mlMwARMwASaIoD4sKmkN4SqHVT5wGPiS+Fou0l6nyREi/mSpkl6TQj/aOqE3skETMAETMAETMAETGDdErBQsW75++wmYAImYAK1CbwtCBQvldQfNsODAjHiaEmxhOl6kqgEMkXSHElzDdUETMAETMAETMAETKBzCVio6Nxn5ys3ARMwgW4nQLjH60PizDGS+oJw8WpJ/HGSzG7vAb4/EzABEzABEzCBUhKwUFHKx+6bNgETMIGOIZAuT3pCyEOxZ7iDN0m6JOSs6Jib8oWagAmYgAmYgAmYgAnUJmChwr3DBEzABEygEwhE74njJZGn4gBJ7wkVPyhJensn3ISv0QRMwARMwARMwARMIJuAhYpsRt7CBEzABExg3ROIQsUxkvCmuEHSaZIODlU/1v0V+gpMwARMwARMwARMwAQKIWChohCMPogJmIAJmECbCLxR0lkh1ONIV/doE3WfxgRMwARMwARMwATaSMBCRRth+1QmYAImYAItE9hJ0i2SdpR0R8tH8wFMwARMwARMwARMwASGHQELFcPukfhpS/hCAAATsElEQVSCTMAETMAEMghMkLTYlEzABEzABEzABEzABLqTgIWK7nyuvisTMAETMAETMAETMAETMAETMAET6EgCFio68rH5ok3ABEzABEzABEzABEzABEzABEygOwlYqOjO5+q7MgETMAETMAETMAETMAETMAETMIGOJGChoiMfmy/aBEzABEzABEzABEzABEzABEzABLqTgIWK7nyuvisTMAETMAETMAETMAETMAETMAET6EgCFio68rH5ok3ABEzABEzABEzABEzABEzA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2B5mJCYlkebWoc/hcQCzWP0kz4sMS0J/MPZjSAt9GWOWSh5JkYDVf7wYYM9zgTv9n/6BpwGJNvE8yGqNChWEBJGIlvsk5ANvC/o7XivfkYR3ylC0rGcSn3HyWT4veALxvpCAk+vEQ4VKIHNTF9moUIE3TgyNIicGfauZ5mfeDDXvYwImYAIdRMBCRQc9LF+qCZiACZjAsCWA2IDYgpcJDYMY4zkmBE2HSQzbG/GFmYAJmIAJmIAJmMC6JmChYl0/AZ/fBEzABEygGwjEFXY8JmIFh+hJwv/xJrm5G27U92ACJmACJmACJmACQ03AQsVQE/bxTcAETMAEykCA0AhCWcjrMC2EMeAWT2WTLyfyfZSBhe/RBEzABEzABEzABFoiYKGiJXze2QRMwARMwARMwARMwARMwARMwARMoEgCFiqKpOljmYAJmIAJmIAJmIAJmIAJmIAJmIAJtETAQkVL+LyzCZiACZiACZiACZiACZiACZiACZhAkQQsVBRJ08cyARMwARMwARMwARMwARMwARMwARNoiYCFipbweWcTMAETMAETMAETMAETMAETMAETMIEiCVioKJKmj2UCJmACJmACJmACJmACJmACJmACJtASAQsVLeHzziZgAiZgAiZgAiZgAiZgAiZgAiZgAkUSsFBRJE0fywRMwARMwARMwARMwARMwARMwARMoCUCFipawuedTcAETMAETMAETMAETMAETMAETMAEiiRgoaJImj6WCZiACZiACZiACZiACZiACZiACZhASwQsVLSEzzubgAmYgAmYgAmYgAmYgAmYgAmYgAkUScBCRZE0fSwTMAETMAETMAETMAETMAETMAETMIGWCFioaAmfdzYBEzABEzABEzABEzABEzABEzABEyiSgIWKImn6WCZgAiZgAiZgAiZgAiZgAiZgAiZgAi0RsFDREj7vbAImYAImYAImYAImYAImYAImYAImUCQBCxVF0vSxTMAETMAETMAETMAETMAETMAETMAEWiJgoaIlfN7ZBEzABEzABEzABEzABEzABEzABEygSAIWKoqk6WOZgAmYgAmYgAmYgAmYgAmYgAmYgAm0RMBCRUv4vLMJmIAJmIAJmIAJmIAJmIAJmIAJmECRBCxUFEnTxzIBEzABEzABEzABEzABEzABEzABE2iJgIWKlvB5ZxMwARMwARMwARMwARMwARMwARMwgSIJWKgokqaPZQImYAImYAImYAImYAImYAImYAIm0BIBCxUt4fPOJmACJmACJmACJmACJmACJmACJmACRRKwUFEkTR/LBEzABEzABEzABEzABEzABEzABEygJQIWKlrC551NwARMwARMwARMwARMwARMwARMwASKJGChokiaPpYJmIAJmIAJmIAJmIAJmIAJmIAJmEBLBCxUtITPO5uACZiACZiACZiACZiACZiACZiACRRJwEJFkTR9LBMwARMwARMwARMwARMwARMwARMwgZYIWKhoCZ93NgETMAETMAETMAETMAETMAETMAETKJKAhYoiafpYJmACJmACJmACJmACJmACJmACJmACLRGwUNESPu9sAiZgAiZgAiZgAiZgAiZgAiZgAiZQJAELFUXS9LFMwARMwARMwARMwARMwARMwARMwARaIvD/AVZGXSXCZxiqAAAAAElFTkSuQmCC" width="799.4999761730439">



```python
# Use Pandas to calcualte the summary statistics for the precipitation data
precip_df.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>prcp</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>365.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>0.169987</td>
    </tr>
    <tr>
      <th>std</th>
      <td>0.295722</td>
    </tr>
    <tr>
      <th>min</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>0.008571</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>0.070000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>0.191667</td>
    </tr>
    <tr>
      <th>max</th>
      <td>2.380000</td>
    </tr>
  </tbody>
</table>
</div>



# Station Analysis


```python
# Use inspector to view table details
for table_name in inspector.get_table_names():
    for column in inspector.get_columns(table_name):
        print( table_name,": ", column.get('name'), ", ", column.get('type'))
```

    measurement :  id ,  INTEGER
    measurement :  station ,  TEXT
    measurement :  date ,  TEXT
    measurement :  prcp ,  FLOAT
    measurement :  tobs ,  FLOAT
    station :  id ,  INTEGER
    station :  station ,  TEXT
    station :  name ,  TEXT
    station :  latitude ,  FLOAT
    station :  longitude ,  FLOAT
    station :  elevation ,  FLOAT



```python
# How many stations are available in this dataset?
station_list = session.query(Station.id,Station.station,Station.name)
print(f"There are {station_list.count()} stations in the dataset")
```

    There are 9 stations in the dataset



```python
# List the stations and the counts in descending order.
station_activity = session.query(Measurement.station,
                  func.count(Measurement.station))\
.group_by(Measurement.station)\
.order_by(func.count(Measurement.station).desc())
for row in station_activity:
    print(row)
```

    ('USC00519281', 2772)
    ('USC00519397', 2724)
    ('USC00513117', 2709)
    ('USC00519523', 2669)
    ('USC00516128', 2612)
    ('USC00514830', 2202)
    ('USC00511918', 1979)
    ('USC00517948', 1372)
    ('USC00518838', 511)



```python
# What are the most active stations? 
highest_station_activity = session.query(Measurement.station,
                  func.count(Measurement.station))\
.group_by(Measurement.station)\
.order_by(func.count(Measurement.station).desc()).limit(1).scalar()
print(f"The station with the hightest number of observations is {highest_station_activity}. ")
```

    The station with the hightest number of observations is USC00519281. 



```python
# Using the station id from the previous query, calculate the lowest temperature recorded, 
#    highest temperature recorded, and average temperature most active station?

q = session.query(Station.id,
                  Station.name,
                  func.min(Measurement.tobs),
                  func.max(Measurement.tobs),
                  func.avg(Measurement.tobs))\
.filter(Measurement.station == Station.station)\
.filter(Measurement.station == "USC00519281")
avg_tmp_rec = "{0:.1f}".format(q[0][4])
print(f"Most Active Station ID: {q[0][0]}, \
    Name: {highest_station_activity},\
    Location: {q[0][1]} \nResults: \n    Minimum temperature recorded:  {q[0][2]}\n\
    Maximum temperture recorded :  {q[0][3]}\n    Average temperature recorded:  {avg_tmp_rec}")
```

    Most Active Station ID: 7,     Name: USC00519281,    Location: WAIHEE 837.5, HI US 
    Results: 
        Minimum temperature recorded:  54.0
        Maximum temperture recorded :  85.0
        Average temperature recorded:  71.7



```python
# Choose the station with the highest number of temperature observations = (highest_station_activity)
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
tobs_twelve = session.query(Measurement.tobs)\
    .filter(Measurement.date > year_ago)\
    .filter(Measurement.station == highest_station_activity)\
    .order_by(Measurement.tobs).all()
    
for row in tobs_twelve:
    print(row)
```

    (59.0,)
    (59.0,)
    (59.0,)
    (60.0,)
    (60.0,)
    (61.0,)
    (62.0,)
    (62.0,)
    (62.0,)
    (62.0,)
    (62.0,)
    (62.0,)
    (63.0,)
    (63.0,)
    (63.0,)
    (63.0,)
    (64.0,)
    (64.0,)
    (64.0,)
    (65.0,)
    (65.0,)
    (65.0,)
    (65.0,)
    (65.0,)
    (65.0,)
    (65.0,)
    (66.0,)
    (66.0,)
    (66.0,)
    (66.0,)
    (66.0,)
    (67.0,)
    (67.0,)
    (67.0,)
    (67.0,)
    (67.0,)
    (67.0,)
    (67.0,)
    (67.0,)
    (67.0,)
    (67.0,)
    (67.0,)
    (67.0,)
    (67.0,)
    (67.0,)
    (67.0,)
    (68.0,)
    (68.0,)
    (68.0,)
    (68.0,)
    (68.0,)
    (68.0,)
    (68.0,)
    (68.0,)
    (68.0,)
    (68.0,)
    (68.0,)
    (68.0,)
    (69.0,)
    (69.0,)
    (69.0,)
    (69.0,)
    (69.0,)
    (69.0,)
    (69.0,)
    (69.0,)
    (69.0,)
    (69.0,)
    (69.0,)
    (69.0,)
    (69.0,)
    (69.0,)
    (69.0,)
    (69.0,)
    (69.0,)
    (69.0,)
    (69.0,)
    (70.0,)
    (70.0,)
    (70.0,)
    (70.0,)
    (70.0,)
    (70.0,)
    (70.0,)
    (70.0,)
    (70.0,)
    (70.0,)
    (70.0,)
    (70.0,)
    (70.0,)
    (70.0,)
    (70.0,)
    (70.0,)
    (70.0,)
    (70.0,)
    (70.0,)
    (70.0,)
    (70.0,)
    (70.0,)
    (71.0,)
    (71.0,)
    (71.0,)
    (71.0,)
    (71.0,)
    (71.0,)
    (71.0,)
    (71.0,)
    (71.0,)
    (71.0,)
    (71.0,)
    (71.0,)
    (71.0,)
    (71.0,)
    (71.0,)
    (71.0,)
    (71.0,)
    (71.0,)
    (72.0,)
    (72.0,)
    (72.0,)
    (72.0,)
    (72.0,)
    (72.0,)
    (72.0,)
    (72.0,)
    (72.0,)
    (72.0,)
    (72.0,)
    (72.0,)
    (72.0,)
    (72.0,)
    (72.0,)
    (72.0,)
    (72.0,)
    (72.0,)
    (72.0,)
    (72.0,)
    (72.0,)
    (72.0,)
    (73.0,)
    (73.0,)
    (73.0,)
    (73.0,)
    (73.0,)
    (73.0,)
    (73.0,)
    (73.0,)
    (73.0,)
    (73.0,)
    (73.0,)
    (73.0,)
    (73.0,)
    (73.0,)
    (73.0,)
    (73.0,)
    (73.0,)
    (73.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (74.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (75.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (76.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (77.0,)
    (78.0,)
    (78.0,)
    (78.0,)
    (78.0,)
    (78.0,)
    (78.0,)
    (78.0,)
    (78.0,)
    (78.0,)
    (78.0,)
    (78.0,)
    (78.0,)
    (78.0,)
    (78.0,)
    (78.0,)
    (78.0,)
    (78.0,)
    (78.0,)
    (78.0,)
    (78.0,)
    (78.0,)
    (78.0,)
    (79.0,)
    (79.0,)
    (79.0,)
    (79.0,)
    (79.0,)
    (79.0,)
    (79.0,)
    (79.0,)
    (79.0,)
    (79.0,)
    (79.0,)
    (79.0,)
    (79.0,)
    (79.0,)
    (79.0,)
    (79.0,)
    (79.0,)
    (79.0,)
    (80.0,)
    (80.0,)
    (80.0,)
    (80.0,)
    (80.0,)
    (80.0,)
    (80.0,)
    (80.0,)
    (80.0,)
    (80.0,)
    (80.0,)
    (81.0,)
    (81.0,)
    (81.0,)
    (81.0,)
    (82.0,)
    (82.0,)
    (82.0,)
    (83.0,)



```python
tobs_df = pd.DataFrame(tobs_twelve, columns=['temp'])
tobs_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>temp</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>59.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>59.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>59.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>60.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>60.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Plot Temperature Results for Most Active Station
plt.subplots(figsize=(8,5))

plt.hist(tobs_df['temp'], bins=12, color="mediumblue", alpha=.7)
plt.title(f"Temperature Results for station {highest_station_activity}\n Date Range: \
{year_ago} - {rec_date}",fontsize=12)
plt.xlabel('Temperature Bins (12)', fontsize=12)
plt.ylabel("Frequency", fontsize=12)
labels = ['temp']
plt.legend(labels)
plt.gcf().subplots_adjust(bottom=0.15)
plt.tight_layout()
plt.savefig('temperature_results_hist.png')
plt.show()
```


    <IPython.core.display.Javascript object>



<img src="data:image/png;base64,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" width="799.4999761730439">


# Temperature Analysis

### Modified Function (Def) to handle varied trip dates per query; accommodates for data updates.


```python
# NEW CODE - Modified for variable trip dates and data updates


def calc_temps(trip_start_date, trip_end_date, most_recent_date):
    
    # Prepare date specifics  for selecting proper year for query
    m_yr = most_recent_date[0:4]
    m_md = str(most_recent_date[5:7]) + str(most_recent_date[8:10])
    if m_md[0:1] == "0":
        m_md = m_md[1:] # (MonthDay) eval will not work on a string starting with zero
        
    # Allow for updates to the data file to accomodate for same year conditions or older trip dates
    t_yr = trip_end_date[0:4]
    t_md = str(trip_end_date[5:7]) + str(trip_end_date[8:10])
    if t_md[0:1] == "0":
        t_md = t_md[1:]

    # Figure it out for the year adjustement     
    if (eval(t_yr) > eval(m_yr) and eval(m_md) >= eval(t_md)):
        yr_adjust = 0
    elif eval(t_yr) < eval(m_yr) and eval(t_md) <= eval(m_md):
        yr_adjust = 0
    else:
        yr_adjust = 1   
    
    # Build dates for past data per time frame - Get most recent year's data for the trip days
    #rec_date = str(most_recent_date)[2:-3]
    search_start_date = str(eval(most_recent_date[0:4])-yr_adjust) + trip_start_date[4:]
    search_end_date = str(eval(most_recent_date[0:4])-yr_adjust) + trip_end_date[4:]
    # existing code from supplied notebook: modified and cleaned up
    trip_stats = session.query(func.min(Measurement.tobs),
                               func.avg(Measurement.tobs),
                               func.max(Measurement.tobs))\
    .filter(Measurement.date >= search_start_date)\
    .filter(Measurement.date <= search_end_date).all()
    TMIN = trip_stats[0][0]
    TAVG = trip_stats[0][1]
    TMAX = trip_stats[0][2]
    
    return TMIN, TAVG, TMAX, search_start_date, search_end_date
```


```python
# Calculate the date 1 year ago from today - re-posted here for reference
most_recent_date = session.query(Measurement.date)\
    .order_by(Measurement.date.desc()).first() 
most_recent_date = most_recent_date[0]
```

### Select your START and END dates for query and RE_RUN cell


```python
# Hard code trip dates in lieu of webside request

# RE_RUN this cell with sample dates below.  TEST results will print below cell

# The function is written to work with updated data as well
# All queryies will return the most recent year's data for the month/day time period

# --Will use 2016 data because there is no data after 2017-08-23 at the time of this code
start_date = "2018-11-10"
end_date = "2018-11-24"

# --Will use 2017 data
# start_date = "2018-01-10"
# end_date = "2018-01-24"

# --Will use 2016 data because there is no data after 2017-08-23 at the time of this code
# start_date = "2017-12-01"
# end_date = "2017-12-15"

# --Will use 2016 data because there is no data after 2017-08-23 at the time of this code
# start_date = "2011-11-10"
# end_date = "2011-11-24"

# Process dates for appropriate year's data query
TMIN, TAVG, TMAX, search_sd, search_ed = calc_temps(start_date, end_date, most_recent_date)
tmp_avg = "{0:.1f}".format(TAVG)

# Print RESULTS:
print()
print(f"Most recent termperature data available is up until:\n  {most_recent_date}")
print()
print(f"Trip Start and End dates:\n  {start_date}\n  {end_date}")
print(f"Calculated Search Dates based on Trip Ending Date:\n  {search_sd}\n  {search_ed}")
print(f"RESULTS:\n  Temp Min: {TMIN}  Temp Avg: {tmp_avg}  Temp: {TMAX}")
```

    
    Most recent termperature data available is up until:
      2017-08-23
    
    Trip Start and End dates:
      2018-11-10
      2018-11-24
    Calculated Search Dates based on Trip Ending Date:
      2016-11-10
      2016-11-24
    RESULTS:
      Temp Min: 67.0  Temp Avg: 74.8  Temp: 80.0



```python
# Plot figure for Trip Ave Temp
plt.subplots(figsize=(6,5))
plt.xlim(0, 2)
plt.ylim([0,110])
plt.bar(1, TAVG, color = 'orange', yerr = TMAX-TMIN, tick_label="", align='center')
plt.title(f"Trip Ave Temp\n Historical Data from:  {search_sd} - {search_ed}", fontsize=14)
plt.ylabel("Temp (F)")
plt.tight_layout()

plt.show()
plt.savefig('trip_ave_temp.png')
```


    <IPython.core.display.Javascript object>



<img src="data:image/png;base64,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gAABAgQIVBAQQCqgO5IAAQIECBAgQIDArAICyKyT1zcBAgQIECBAgACBCgICSAV0RxIgQIAAAQIECBCYVUAAmXXy+iZAgAABAgQIECBQQUAAqYDuSAIECBAgQIAAAQKzCgggs05e3wQIECBAgAABAgQqCAggFdAdSYAAAQIECBAgQGBWAQFk1snrmwABAgQIECBAgEAFAQGkArojCRAgQIAAAQIECMwqIIDMOnl9EyBAgAABAgQIEKggIIBUQHckAQIECBAgQIAAgVkFBJBZJ69vAgQIECBAgAABAhUEBJAK6I4kQIAAAQIECBAgMKuAADLr5PVNgAABAgQIECBAoIKAAFIB3ZEECBAgQIAAAQIEZhUQQGadvL4JECBAgAABAgQIVBAQQCqgO5IAAQIECBAgQIDArAICyKyT1zcBAgQIECBAgACBCgICSAV0RxIgQIAAAQIECBCYVUAAmXXy+iZAgAABAgQIECBQQUAAqYDuSAIECBAgQIAAAQKzCgggs05e3wQIECBAgAABAgQqCAggFdAdSYAAAQIECBAgQGBWAQFk1snrmwABAgQIECBAgEAFAQGkArojCRAgQIAAAQIECMwqIIDMOnl9EyBAgAABAgQIEKgg8H8r6rCZudTklQAAAABJRU5ErkJggg==" width="599.9999821186071">



```python
# Calculate the rainfall per weather station for your trip dates using the previous year's matching dates.
# Sort this in descending order by precipitation amount and list the station, name, latitude, longitude, 
# and elevation

q = session.query(Station.station,
                  func.sum(Measurement.prcp),
                  Station.name,
                  Station.elevation,                                    
                  Station.latitude,
                  Station.longitude)\
.filter(Measurement.station == Station.station)\
.filter(Measurement.date >= search_sd)\
.filter(Measurement.date <= search_ed)\
.group_by(Station.station)\
.order_by(func.sum(Measurement.prcp).desc())

# A nice layout to read the results
print()
print (f"Historical Rainfall Per Weather Station - Descending order\n  Trip Dates: \
{start_date} - {end_date}\n  Most Recent Data Search Dates: {search_sd} - {search_ed}")
print()
for row in q:
    rain="{0:.2f}".format(row[1])
    print (f"Station:  {row[0]}\n    Rainfall:  {rain}  \n    Location:  {row[2]}\n    Elevation:  {row[3]}  \
    Latitude:  {row[4]}  Longitude:  {row[5]}")
    print()       
```

    
    Historical Rainfall Per Weather Station - Descending order
      Trip Dates: 2018-11-10 - 2018-11-24
      Most Recent Data Search Dates: 2016-11-10 - 2016-11-24
    
    Station:  USC00516128
        Rainfall:  6.93  
        Location:  MANOA LYON ARBO 785.2, HI US
        Elevation:  152.4      Latitude:  21.3331  Longitude:  -157.8025
    
    Station:  USC00519281
        Rainfall:  3.46  
        Location:  WAIHEE 837.5, HI US
        Elevation:  32.9      Latitude:  21.45167  Longitude:  -157.84888999999998
    
    Station:  USC00519523
        Rainfall:  1.24  
        Location:  WAIMANALO EXPERIMENTAL FARM, HI US
        Elevation:  19.5      Latitude:  21.33556  Longitude:  -157.71139
    
    Station:  USC00513117
        Rainfall:  1.12  
        Location:  KANEOHE 838.1, HI US
        Elevation:  14.6      Latitude:  21.4234  Longitude:  -157.8015
    
    Station:  USC00519397
        Rainfall:  0.41  
        Location:  WAIKIKI 717.2, HI US
        Elevation:  3.0      Latitude:  21.2716  Longitude:  -157.8168
    
    Station:  USC00514830
        Rainfall:  0.23  
        Location:  KUALOA RANCH HEADQUARTERS 886.9, HI US
        Elevation:  7.0      Latitude:  21.5213  Longitude:  -157.8374
    
    Station:  USC00517948
        Rainfall:  0.02  
        Location:  PEARL CITY, HI US
        Elevation:  11.9      Latitude:  21.3934  Longitude:  -157.9751
    



```python
break
```


      File "<ipython-input-34-6aaf1f276005>", line 1
        break
             ^
    SyntaxError: 'break' outside loop



# STEP 2 - CLIMATE APP


```python
# Design a Flask API based on the queries that you have just developed.
#   USE Flask to create your routes
```

## Code from Hawaii_app.py and db_prepare.py 



```python
# Hawaii_app.py by Verna Orsatti
# Use in combination with db_prepare.py for boilerplate SQLalchemy 
from flask import Flask, json, jsonify
from db_prepare import engine, func, session, Measurement, Station

app = Flask(__name__)

# CLASSES
# measurement :  id ,  INTEGER
# measurement :  station ,  TEXT
# measurement :  date ,  TEXT
# measurement :  prcp ,  FLOAT
# measurement :  tobs ,  FLOAT
# station :  id ,  INTEGER
# station :  station ,  TEXT
# station :  name ,  TEXT
# station :  latitude ,  FLOAT
# station :  longitude ,  FLOAT
# station :  elevation ,  FLOAT
```


```python
@app.route('/')
def home_route():
    """ Available API Route Endpoints"""
    return (f"Enter Available Route Endpoints.  Where dates are required, modify date selection as desired: <br><br/>"
        f"1.   2017 dates & temps dictionary:   <br/>"
        f"   /api/v1.0/precipitation/ <br><br/>" 
        f"2.   JSON list of stations:    <br/>"
        f" /api/v1.0/stations/ <br><br/>" 
        f"3.    2017 JSON list of Temp Observations:  <br/>"
        f" /api/v1.0/tobs/ <br><br/>"
        f"For the following, enter date as form 'yyyy' or 'yyyy-mm' or 'yyyy-mm-dd' for BEST RESULTS! <br><br/>"
        f"4.    Stats Combined Stations. Enter Start date:  <br/>"
        f" /api/v1.0/2016-01-01/ <br><br/>" 
        f"5.    Stats Combined Stations. Enter Start & End Date:  <br/>"
        f" /api/v1.0/2016-01-01/2016-12-31/ <br><br/>"
        f"BONUS Options for the interested! <br><br/>"
        f"6.    Stats by Station,  Enter Start date:    <br/>"
        f"  /api/v1.0/station/2017-01-01/ <br><br/>" 
        f"7.    Stats by Station,  Enter Start & End date:   <br/>"
        f"   /api/v1.0/station/2016-01-01/2016-12-31/ <end>")
        
```


```python
#    Query Measurements for... All Stations
#    Dates and temperature observations from the last year.
#    Convert the query results to a Dictionary using 'date' as the key and 'tobs' as the value.
#    Return the JSON representation of your dictionary
@app.route('/api/v1.0/precipitation/')
def precipitation():
    prcp_results = session.query(Measurement.date, Measurement.tobs)\
    .filter(Measurement.date >= '2017-01-01').all()
    p_dict = dict(prcp_results)
    print()
    print("Results for Precipitation")
    return jsonify(p_dict) 
```


```python
#    Query Stations for.... Stations
#    Return a JSON-list of stations from the dataset.
@app.route('/api/v1.0/stations/')
def stations():
    station_list = session.query(Station.station)\
    .order_by(Station.station).all() 
    print()
    print("Station List:")   
    for row in station_list:
        print (row[0])
    return jsonify(station_list)
```


```python
#    Query Measurement for.... All stations
#    Return a JSON-list of Temperature Observations from the dataset.
@app.route('/api/v1.0/tobs/')
def tobs():
    temp_obs = session.query(Measurement.tobs)\
    .order_by(Measurement.date).all()
    print()
    print("Temperature Results for All Stations")
    return jsonify(temp_obs)
```


```python
# Query Measurements for.... Combined Stations
# Return a JSON-list of Temperature Observations from the previous year.
#   /api/v1.0/<start  and /api/v1.0/<start>/<end>
#   Return JSON list of temps: minimum, average, maxium as TMIN TAVG TMAX
#       FOR A GIVEN START DATE OR START END RANGE
@app.route('/api/v1.0/<start>/')
def combined_start_stats(start):
    q = session.query(Station.id,
                  Station.station,
                  func.min(Measurement.tobs),
                  func.max(Measurement.tobs),
                  func.avg(Measurement.tobs))\
                  .filter(Measurement.station == Station.station)\
                  .filter(Measurement.date >= start).all()                  
    print()
    print("Query Temps Combinded Stations with Start ({start}) Date")
    for row in q:
        print()
        print(row)
    return jsonify(q)
```


```python
# Query Measurements for.... Combined Stations
# Repeat of above stat request, but with end date added to decorator
@app.route('/api/v1.0/<start>/<end>/')
def combined_start_end_stats(start,end):
    q = session.query(Station.id,
                  Station.station,
                  func.min(Measurement.tobs),
                  func.max(Measurement.tobs),
                  func.avg(Measurement.tobs))\
                  .filter(Measurement.station == Station.station)\
                  .filter(Measurement.date <= end)\
                  .filter(Measurement.date >= start).all()
    print()
    print(f"Query Temps Combined Stations with Start ({start}) and End ({end}) Date")
    for row in q:
        print()
        print(row)
    return jsonify(q)
```


```python
# BONUS options for the interested!

#    Query Measurements for.... by Station
#    Return a JSON-list of Temperature Observations from the previous year.
#   /api/v1.0/<start  and /api/v1.0/<start>/<end>
#   Return JSON list of temps: minimum, average, maxium as TMIN TAVG TMAX
#       FOR A GIVEN START DATE OR START END RANGE
@app.route('/api/v1.0/station/<start>/')
def station_start_stats(start):
    q = session.query(Station.id,
                  Station.station,
                  func.min(Measurement.tobs),
                  func.max(Measurement.tobs),
                  func.avg(Measurement.tobs))\
                  .filter(Measurement.station == Station.station)\
                  .filter(Measurement.date >= start)\
                  .group_by(Station.station)\
                  .order_by(Station.id).all()
    print()
    print("Query Temps for Stations with Start ({start}) Date")
    for row in q:
        print()
        print(row)
    return jsonify(q)
```


```python
# Query Measurements for.... by Station
# Repeat of above stat request, but with end date added to decorator
@app.route('/api/v1.0/station/<start>/<end>/')
def station_start_end_stats(start,end):
    q = session.query(Station.id,
                  Station.station,
                  func.min(Measurement.tobs),
                  func.max(Measurement.tobs),
                  func.avg(Measurement.tobs))\
                  .filter(Measurement.station == Station.station)\
                  .filter(Measurement.date <= end)\
                  .filter(Measurement.date >= start)\
                  .group_by(Station.station)\
                  .order_by(Station.id).all()
    print()
    print(f"Query Temps for Stations with Start ({start}) and End ({end}) Date")
    for row in q:
        print()
        print(row)
    return jsonify(q)
```


```python
app.run(debug=True)
```


```python
## SQLalchemy Boilerplate:  db_prepare.py
```


```python
# db_prepare.py

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#engine = create_engine("sqlite:///../Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
```

### It was real... it was fun... but not real fun" ~anonymous quote from the '70s
