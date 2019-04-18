# HW4 Utilize Hadoop for Dataset Analysis

### Command line used to run MapReduce
```
hadoop jar /usr/hdp/2.6.3.0-235/hadoop-mapreduce/hadoop-streaming-2.7.3.2.6.3.0-235.jar -file mapper.py 

-mapper mapper.py -file reducer.py -reducer reducer.py -input /data/nyc/nyc-traffic.csv -output mr
```

* Hadoop Jar File - "/usr/hdp/2.6.3.0-235/hadoop-mapreduce/hadoop-streaming-2.7.3.2.6.3.0-235.jar" 
* Mapper File - mapper.py 
* Reducer File - reducer.py 
