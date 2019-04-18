#!/usr/bin/env python
from __future__ import print_function
from pyspark import SparkContext
from pyspark.sql import SQLContext, Row

sc = SparkContext.getOrCreate() #appName='weatherStats')
sqlc = SQLContext(sc)

available_years = range(2000, 2019)  # all data from 2000-2018


def mkdf(filename):
    """
    Read filename (or glob; things like '20??.csv' will work) and return a
    handle to a PySpark DataFrame
    """
    raw = sc.textFile(filename)
    data = raw.map(lambda x: x.split(','))
    table = data.map(lambda r: Row(sta=r[0], date=r[1], meas=r[2],
                                   degc=int(r[3]), m=r[4], q=r[5], s=r[6],
                                   time=r[7]))
    df = sqlc.createDataFrame(table)
    return df.filter(df.q=='')  # prune measurements w/ quality problems


def run(years=available_years):
    """
    Run analyses on individual years in sequence
    """
    import pyspark.sql.functions as sqlf

    # allow passing a single year or a list of them
    if not type(years) is list:
        years = [years]

    for year in years:
        if not year in available_years:
            raise RuntimeError('Sorry, %s is not available in the dataset.' % year)

        df = mkdf('data/%s.csv' % year)

        print("\n%s\n====\n" % year)


        # Lowest TMIN
        r = df.filter(df.meas=='TMIN').groupBy().min('degc').first()
        print('Min TMIN = %0.1f deg C' % (r['min(degc)'] / 10.0))

        # Highest TMAX
        r = df.filter(df.meas=='TMAX').groupBy().max('degc').first()
        print('Max TMAX = %0.1f deg C' % (r['max(degc)'] / 10.0))

        
        # Average TMIN
        r = df.filter(df.meas=='TMIN').groupBy().avg('degc').first()
        print('Avg TMIN = %0.1f deg C' % (r['avg(degc)'] / 10.0))

        # Average TMAX
        r = df.filter(df.meas=='TMAX').groupBy().avg('degc').first()
        print('Avg TMAX = %0.1f deg C' % (r['avg(degc)'] / 10.0))

        # Median TMIN
        r = df.filter(df.meas=='TMIN').approxQuantile('degc',[0.5], 0.25)
        print('Median TMIN = %0.1f deg C' % (r[0] / 10.0))
        
        # Median TMAX
        r = df.filter(df.meas=='TMAX').approxQuantile('degc',[0.5], 0.25)
        print('Median TMAX = %0.1f deg C' % (r[0] / 10.0))


        # Five hottest stations (on average)
        fivehot = df.filter(df.meas=='TMAX') \
                    .groupBy(df.sta) \
                    .agg(sqlf.avg('degc')) \
                    .sort(sqlf.desc('avg(degc)')) \
                    .limit(5).collect()
        print()
        i = 1
        for s in fivehot:
            t = float(s['avg(degc)']) / 10.0
            print('Hottest station #%s: %s - %0.1f deg C'
                  % (i, s.sta, t))
            i = i + 1

        # Five coldest stations (on average)
        fivecold = df.filter(df.meas=='TMIN') \
                     .groupBy(df.sta) \
                     .agg(sqlf.avg('degc')) \
                     .sort(sqlf.asc('avg(degc)')) \
                     .limit(5).collect()
        print()
        i = 1
        for s in fivecold:
            t = float(s['avg(degc)']) / 10.0
            print('Coldest station #%s: %s - %0.1f deg C'
                  % (i, s.sta, t))
            i = i + 1


def run_whole_dataset():
    """
    Run analyses over the entire dataset
    """
    import pyspark.sql.functions as sqlf
    from datetime import datetime as dt

    # Hottest and coldest day and corresponding weather stations in the
    # entire dataset
    print("\nEntire dataset (2000-2018)\n==========================\n")
    print('  * Loading all datasets into a single DataFrame...')
    df = mkdf('data/20??.csv')

 
    # coldest station
    print('  * Computing coldest station for entire dataset...\n')
    coldest = df.filter(df.meas=='TMIN').groupBy('sta', 'date').min('degc') \
                .sort(sqlf.asc('min(degc)')).first()

    date = dt.strptime(coldest.date, '%Y%m%d').strftime('%d %b %Y')

    print('Coldest station was %s on %s: %0.1f deg C'
          % (coldest.sta, date, float(coldest['min(degc)']) / 10.0))

    # and now the hottest
    print('\n  * Computing hottest station for entire dataset...\n')
    hottest = df.filter(df.meas=='TMAX').groupBy('sta', 'date').max('degc') \
                .sort(sqlf.desc('max(degc)')).first()

    date = dt.strptime(hottest.date, '%Y%m%d').strftime('%d %b %Y')

    print('Hottest station was %s on %s: %0.1f deg C'
          % (hottest.sta, date, float(hottest['max(degc)']) / 10.0))

    # Median TMIN
    print('\n  * Computing median TMIN for entire dataset...\n')
    TMIN_m = df.filter(df.meas=='TMIN').approxQuantile('degc',[0.5], 0.25)
    print('Median TMIN for the entire dataset: %0.1f deg C' % (TMIN_m[0] / 10.0))

    # Median TMAX
    print('\n  * Computing median TMAX for entire dataset...\n')
    TMAX_m = df.filter(df.meas=='TMAX').approxQuantile('degc',[0.5], 0.25)
    print('Median TMAX for the entire dataset: %0.1f deg C' % (TMAX_m[0] / 10.0))

if __name__ == '__main__':
    run()
