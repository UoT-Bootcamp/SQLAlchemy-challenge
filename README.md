# SQLAlchemy-challenge

# SURF Up!

I have decided to treat myself to a long holiday vacation in Honolulu, Hawaii! To plan the trip, I need to do some climate analysis on the area.


# Precipitation Analysis

I decided to do precipitaion analysis. For this, I need to perform following steps:

* Design a query to retrieve the last 12 months of precipitation data.
* Select only the date and prcp values.
* Load the query results into a Pandas DataFrame and set the index to the date column.
* Sort the DataFrame values by date.
* Plot the results using the DataFrame plot method.
* We will use Pandas to print the summary statistics for the precipitation data.


# Station Analysis

For station analysis, I will do following analysis:

* Design a query to calculate the total number of stations.
* Design a query to find the most active stations.
* List the stations and observation counts in descending order.
* We will use a function such as func.min, func.max, func.avg, and func.count to know whic station has the highest number of observations.
* Design a query to retrieve the last 12 months of temperature observation data (TOBS).
* Filter by the station with the highest number of observations.
* Finally we will plot the results as a histogram with bins=12.


# Temperature Analysis I

* Hawaii is reputed to enjoy mild weather all year. Is there a meaningful difference between the temperature in, for example, June and December?
* Identify the average temperature in June at all stations across all available years in the dataset. We will do the same for December temperature.
* Use the t-test to determine whether the difference in the means, if any, is statistically significant. Will you use a paired t-test, or an unpaired t-test? Why?


# Temperature Analysis II

* The starter notebook contains a function called calc_temps that will accept a start date and end date in the format %Y-%m-%d. The function will return the minimum, average, and maximum temperatures for that range of dates.
* Use the calc_temps function to calculate the min, avg, and max temperatures for your trip using the matching dates from the previous year (i.e., use "2017-01-01" if your trip start date was "2018-01-01").
* Plot the min, avg, and max temperature from your previous query as a bar chart.
* Use the average temperature as the bar height.
* Use the peak-to-peak (TMAX-TMIN) value as the y error bar (YERR).


# Daily Rainfall Average

* Calculate the rainfall per weather station using the previous year's matching dates.
* Calculate the daily normals. Normals are the averages for the min, avg, and max temperatures.
* We will use a function called daily_normals that will calculate the daily normals for a specific date. This date string will be in the format %m-%d. 
* Create a list of dates for our trip in the format %m-%d. Use the daily_normals function to calculate the normals for each date string and append the results to a list.




