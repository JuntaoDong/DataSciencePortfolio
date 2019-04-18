# Project2 - Big Data Analysis Using MapReduce / Apache Spark

This project will have you perform Data Analysis and processing using MapReduce/ Apache Spark. The Project will use the weather dataset from ​https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/​. This project will use only 19 years of data ( 2000 - 2018) for all the stations starting with US and elements TMAX, TMIN.

## Dataset Generation

For Daily Global Historical Climatology Network (GHCN-DAILY), use following shell script to fetch the compressed csv file and subsequently unzip.

```bash
for i in `seq 2000 2018` do
wget https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/${i}.csv.gz gzip -cd ${i}.csv.gz |
grep -e TMIN -e TMAX | grep ^US > ${i}.csv done
```

## Metadata of GHCN-DAILY

The following information serves as a definition of each field in one line of data covering one station-day. Each field described below is separated by a comma ( , ) and follows the order presented in this document.

+ ID = 11 character station identification code
+ YEAR/MONTH/DAY = 8 character date in YYYYMMDD format (e.g. 19860529 = May 29, 1986)
+ ELEMENT = 4 character indicator of element type
+ DATA VALUE = 5 character data value for ELEMENT
+ M-FLAG = 1 character Measurement Flag
+ Q-FLAG = 1 character Quality Flag
+ S-FLAG = 1 character Source Flag
+ OBS-TIME = 4-character time of observation in hour-minute format (i.e. 0700 =7:00 am)

See section III of the GHCN-Daily ftp://​ftp.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt​ file for an explanation of ELEMENT codes and their units as well as the M-FLAG, Q-FLAGS and S-FLAGS. The OBS-TIME field is populated with the observation times contained in NOAA/NCDC’s Multinetwork Metadata System (MMS).

## Project Requirement

+ Average TMIN, TMAX for each year excluding abnormalities or missing data
+ Maximum TMAX, Minimum TMIN for each year excluding abnormalities or missing data
+ 5 hottest , 5 coldest weather stations for each year excluding abnormalities or missing data
+ Hottest and coldest day and corresponding weather stations in the entire dataset
+ Median TMIN, TMAX for each year and corresponding weather stations
+ Median TMIN, TMAX for the entire dataset

## Usage

In this project, I chose pyspark to solve the the above analysis questions. A python file was first created to define the problem-solving functions. The function​ run()​ was designed to solve the questions according to each year while the function​ run_whole_dataset() ​was used to run the analysis on the whole dataset. By inputting following commands in pyspark, all the questions can be done in a while.

```pyspark
pyspark
>>> from weatherstats import run, run_whole_dataset
>>> run()
>>> [...]
>>> run_whole_dataset
>>> [...]
```

Just for clarification, I choose average of TMAX and TMIN to determine the hottest and coldest stations.

## Result

You can check the raw results in the [log](https://github.com/JuntaoDong/DataSciencePortfolio/blob/master/Cloud%20Computing/Project2/log) file.

**Table1. Annual Statistics**
|      | Min TMIN | Max TMAX | Avg TMIN | Avg TMAX | Median TMIN | Median TMAX |
| ---- | -------- | -------- | -------- | -------- | ----------- | ----------- |
 2000 | -57.8 | 52.2 | 4.4 | 17.6 | 12.8 | 26.1 
 2001 | -52.8 | 52.8 | 4.8 | 17.9 | 26.7 | 28.9 
 2002 | -47.2 | 53.3 | 4.7 | 17.7 | 14.4 | 36.7 
 2003 | -50.0 | 53.3 | 4.9 | 17.7 | 26.7 | 17.8 
 2004 | -53.3 | 51.7 | 4.9 | 17.5 | 6.1 | 18.9 
 2005 | -55.0 | 53.9 | 5.0 | 17.8 | 11.1 | 24.4 
 2006 | -52.8 | 52.8 | 5.1 | 18.1 | 16.1 | 26.7 
 2007 | -53.9 | 55.6 | 4.9 | 17.8 | 8.9 | 30.6 
 2008 | -57.8 | 52.8 | 4.1 | 17.0 | 11.8 | 26.1 
 2009 | -55.6 | 53.3 | 4.3 | 16.9 | 5.6 | 21.7 
 2010 | -53.3 | 51.7 | 4.7 | 17.1 | 5.6 | 19.4 
 2011 | -51.7 | 51.1 | 4.6 | 17.2 | 9.4 | 14.4 
 2012 | -54.4 | 53.7 | 5.3 | 18.4 | 7.8 | 23.9 
 2013 | -52.8 | 53.9 | 4.3 | 16.7 | 16.7 | 23.9 
 2014 | -50.0 | 52.2 | 4.4 | 16.8 | 6.7 | 34.4 
 2015 | -52.8 | 55.6 | 5.3 | 17.7 | 27.2 | 17.8 
 2016 | -46.9 | 53.9 | 5.5 | 17.9 | 11.1 | 20.0 
 2017 | -52.0 | 52.8 | 5.3 | 17.7 | 4.4 | 16.7 
 2018 | -52.8 | 41.7 | -3.2 | 8.6 | -4.3 | 6.7 

**Table2. Annual Hottest Stations and Corresponding Avg TMAX**
|      | Station #1 | Station #2 | Station #3 | Station #4 | Station #5 |
| ---- | ---------- | ---------- | ---------- | ---------- | ---------- |
| 2000 | USC00416892 - 37.4 | USC00411013 - 36.9 | USC00045502 - 36.8 | USC00024761 - 35.0 | USC00021026 - 34.0 |
| 2001 | USC00045502 - 35.6 | USC00022434 - 35.1 | USC00026250 - 34.0 | USC00024761 - 33.9 | USC00042319 - 33.8 |
| 2002 | USC00022807 - 34.6 | USC00347254 - 34.4 | USC00042319 - 33.9 | USC00044259 - 33.4 | USR0000CBUU - 32.8 |
| 2003 | USC00344766 - 36.2 | USC00026194 - 35.1 | USC00045502 - 34.7 | USR0000CWIL - 34.6 | USC00412906 - 34.3 |
| 2004 | USC00042346 - 37.1 | USW00053139 - 34.8 | USR0000CMIO - 34.3 | USW00023195 - 33.7 | USC00044259 - 33.4 | 
| 2005 | USR0000MKIL - 34.0 | USC00290525 - 34.0 | USC00427606 - 33.5 | USC00383906 - 32.9 | USC00311515 - 32.6 |
| 2006 | USC00021514 - 40.8 | USC00419122 - 36.2 | USC00080611 - 35.0 | USR0000HMOL - 34.0 | USC00042319 - 33.4 |
| 2007 | USC00314987 - 38.3 | USC00029376 - 35.5 | USR0000HMOL - 34.6 | USC00042319 - 34.0 | USC00041048 - 33.8 | 
| 2008 | USC00411671 - 35.1 | USC00254113 - 35.0 | USW00003125 - 34.9 | USR0000HMOL - 34.5 | USC00044259 - 34.4 |
| 2009 | USC00141408 - 37.8 | USR0000HMOL - 36.2 | USC00144530 - 36.1 | USC00027370 - 34.5 | USC00046198 - 34.3 | 
| 2010 | USC00141408 - 35.0 | USC00417951 - 34.9 | USC00027370 - 33.4 | USC00028070 - 33.3 | USC00341544 - 33.1 | 
| 2011 | USR0000CTAR - 37.8 | USC00411416 - 37.0 | USC00035514 - 36.1 | USC00412350 - 34.4 | USR0000HMOL - 34.4 | 
| 2012 | USW00012946 - 35.9 | USC00290915 - 35.4 | USC00412906 - 34.8 | USC00040924 - 34.6 | USC00042319 - 34.5 | 
| 2013 | USC00260125 - 36.9 | USC00042319 - 33.7 | USC00042410 - 33.6 | USC00025270 - 33.3 | USC00021050 - 33.0 |
| 2014 | USC00413618 - 36.2 | USC00042319 - 34.7 | USC00040924 - 34.1 | USW00003145 - 33.8 | USC00029656 - 33.6 | 
| 2015 | USC00092593 - 34.6 | USC00403379 - 34.6 | USC00414278 - 34.6 | USC00040924 - 34.4 | USC00042319 - 34.1 |
| 2016 | USC00412906 - 40.5 | USC00297461 - 36.3 | USC00415101 - 35.6 | USC00406340 - 34.3 | USC00025700 - 34.3 |
| 2017 | USC00044297 - 36.6 | USC00022790 - 36.0 | USC00042319 - 34.2 | USC00029656 - 33.9 | USC00020632 - 33.6 | 
| 2018 | USW00092826 - 28.4 | USC00515710 - 28.1 | USW00003104 - 28.0 | USR0000FOAS - 28.0 | USW00092809 - 27.8 |

**Table3. Annual Coldest Stations and Corresponding Avg TMIN**
|      | Station #1 | Station #2 | Station #3 | Station #4 | Station #5 |
| ---- | ---------- | ---------- | ---------- | ---------- | ---------- |
| 2000 | USC00508140 - -20.8 | USC00505873 - -18.7 | USR0000WBAR - -18.1 | USC00247248 - -16.0 | USW00026508 - -15.7 |
| 2001 | USR0000AHAY - -31.7 | USW00026508 - -29.9 | USC00508409 - -18.7 | USW00026440 - -18.5 | USC00509315 - -18.4 |
| 2002 | USR0000NHAM - -19.2 | USS0051R01S - -19.0 | USC00502873 - -17.3 | USC00501987 - -15.1 | USC00263101 - -14.8 |
| 2003 | USS0045M07S - -20.1 | USS0048V01S - -17.8 | USC00433581 - -16.6 | USC00067373 - -16.3 | USC00503181 - -15.7 |
| 2004 | USR0000ACOA - -25.4 | USR0000AOKL - -21.7 | USR0000ASTU - -21.7 | USR0000NLIM - -21.0 | USC00306957 - -19.7 |
| 2005 | USR0000AFYK - -41.1 | USR0000AUMI - -38.3 | USR0000ADEV - -28.9 | USC00305925 - -27.8 | USR0000AWLL - -23.9 |
| 2006 | USC00505534 - -24.2 | USC00508130 - -17.8 | USC00210059 - -17.2 | USS0049T03S - -17.2 | USS0045Q05S - -16.4 |
| 2007 | USC00502707 - -26.0 | USR0000AUMI - -25.4 | USC00248857 - -23.3 | USC00509315 - -20.0 | USC00502107 - -17.1 | 
| 2008 | USS0051R01S - -26.0 | USC00509315 - -24.4 | USC00390223 - -19.7 | USC00391917 - -19.4 | USC00476838 - -19.3 |
| 2009 | USC00501492 - -33.4 | USC00471618 - -30.5 | USC00509315 - -27.5 | USC00502015 - -24.4 | USC00212916 - -23.4 | 
| 2010 | USC00507097 - -24.0 | USR0000MKIL - -22.9 | USC00505873 - -22.8 | USR0000MOSC - -22.8 | USR0000MBRV - -21.8 | 
| 2011 | USC00479012 - -34.4 | USC00509314 - -24.6 | USR0000MOSC - -22.9 | USR0000MBRV - -22.7 | USC00505136 - -22.6 | 
| 2012 | USC00504210 - -28.3 | USC00504971 - -27.5 | USC00503368 - -22.8 | USC00508156 - -22.3 | USR0000MKIL - -22.0 | 
| 2013 | USR0000ASLC - -35.7 | USC00201940 - -24.4 | USR0000MBRV - -21.6 | USR0000ABUU - -20.3 | USC00503212 - -20.3 |
| 2014 | USC00238456 - -25.5 | USC00210746 - -24.9 | USC00210050 - -24.3 | USC00320450 - -23.9 | USC00208680 - -23.3 | 
| 2015 | USC00158551 - -32.2 | USC00210050 - -31.9 | USC00242347 - -24.2 | USC00508130 - -21.8 | USC00503212 - -20.0 |
| 2016 | USC00200234 - -26.6 | USC00507778 - -18.5 | USC00210746 - -17.1 | USC00273860 - -14.0 | USW00027401 - -13.8 |
| 2017 | USC00503567 - -22.9 | USC00503585 - -21.9 | USC00322525 - -17.1 | USC00421590 - -15.7 | USC00253617 - -15.4 | 
| 2018 | USC00210809 - -26.5 | USC00501684 - -26.2 | USR0000AUMI - -25.9 | USS0051R01S - -24.6 | USR0000ABCK - -24.4 |

**Table4. Statistics of Entire Dataset**
| Feature | Content |
| ------- | ------- |
| Coldest Day and Station | USC00501684 on 07 Feb 2008: -57.8 deg C |
| Hottest Day and Station | USR0000HKAU on 13 Feb 2015: 55.6 deg C |
| Median TMIN | 27.8 deg C |
| Median TMAX | 43.3 deg C |