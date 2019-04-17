import configparser


# CONFIG
config = configparser.ConfigParser()
config.read(r'C:\Users\junta\Documents\GitHub\aws crendential\dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS staging_events
    (
        artist          varchar,
        auth            varchar(15),
        firstname       varchar(25),
        gender          char(1),
        iteminsession   int,
        lastname        varchar(25),
        length          float,
        level           char(4),
        location        varchar,
        method          varchar(10),
        page            varchar,
        registration    NUMERIC(18,0),
        sessionid       int,
        song            varchar,
        status          int,
        ts              int8,
        useragent       varchar,
        userid          int
    ) ;
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs
    (
        num_songs           int,
        artist_id           char(18),
        artist_latitude     float,
        artist_longitude    float,
        artist_location     varchar,
        artist_name         varchar,
        song_id             char(18) PRIMARY KEY,
        title               varchar,
        duration            float,
        year                int
    );
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays 
    (
        songplay_id int IDENTITY(1,1) PRIMARY KEY, 
        start_time timestamp NOT NULL sortkey, 
        user_id int NOT NULL distkey, 
        level char(4) NOT NULL, 
        song_id char(18) NOT NULL, 
        artist_id char(18) NOT NULL, 
        session_id int NOT NULL, 
        location varchar, 
        user_agent varchar NOT NULL
    );
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users
    (
        user_id int NOT NULL PRIMARY KEY distkey, 
        first_name varchar(25) NOT NULL, 
        last_name varchar(25) NOT NULL, 
        gender char(1) NOT NULL, 
        level char(4) NOT NULL
    );
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs
    (
        song_id char(18) NOT NULL PRIMARY KEY , 
        title varchar NOT NULL, 
        artist_id char(18) NOT NULL distkey, 
        year int NOT NULL sortkey, 
        duration float NOT NULL
    );
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists
    (
        artist_id char(18) NOT NULL PRIMARY KEY distkey, 
        artist_name varchar NOT NULL, 
        location varchar, 
        lattitude float, 
        longitude float
    );
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time 
    (
        start_time timestamp NOT NULL PRIMARY KEY sortkey distkey, 
        hour int NOT NULL, 
        day int NOT NULL, 
        week int NOT NULL, 
        month int NOT NULL, 
        year int NOT NULL, 
        weekday int NOT NULL
    );
""")

# STAGING TABLES

staging_events_copy = ("""
    COPY staging_events FROM 's3://udacity-dend/log-data'
    CREDENTIALS 'aws_iam_role={}'
    COMPUPDATE OFF region 'us-west-2'
    FORMAT AS JSON 's3://udacity-dend/log_json_path.json';
""").format(config['IAM_ROLE']['ARN'])

staging_songs_copy = ("""
    COPY staging_songs FROM 's3://udacity-dend/song-data'
    CREDENTIALS 'aws_iam_role={}'
    COMPUPDATE OFF region 'us-west-2'
    FORMAT AS JSON 'auto' TRUNCATECOLUMNS;
""").format(config['IAM_ROLE']['ARN'])

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    (SELECT (TIMESTAMP 'epoch' + e.ts/1000 * INTERVAL '1 Second'), e.userid, e.level, s.song_id, s.artist_id, e.sessionid, e.location, e.useragent
    FROM staging_events e JOIN staging_songs s ON (e.artist=s.artist_name AND e.song=s.title)
    WHERE userid IS NOT NULL AND page='NextSong');
""")

user_table_insert = ("""
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    SELECT userid, firstname, lastname, gender, level
    FROM staging_events
    WHERE userid IS NOT NULL;
""")

song_table_insert = ("""
    INSERT INTO songs (song_id, title, artist_id, year, duration)
    SELECT song_id, title, artist_id, year, duration
    FROM staging_songs;
""")

artist_table_insert = ("""
    INSERT INTO artists (artist_id, artist_name, location, lattitude, longitude)
    SELECT artist_id, artist_name, artist_location, artist_latitude, artist_longitude
    FROM staging_songs;
""")

time_table_insert = ("""
    INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT dt, extract(hour FROM dt), extract(day FROM dt), extract(week FROM dt), extract(month FROM dt), extract(year FROM dt), extract(weekday FROM dt)+1
    FROM (SELECT (TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 Second') AS dt FROM staging_events) AS T;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
