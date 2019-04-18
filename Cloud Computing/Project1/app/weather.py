from flask import Flask, request, abort, make_response, jsonify, render_template
from flask_restful import Resource, Api
from sqlalchemy import create_engine
import json
import csv

# The sqlite3 database has been created separately from this file.
# .schema = DATE TEXT, TMAX REAL, TMIN REAL
engine = create_engine('sqlite:///daily.db')

app = Flask(__name__)
api = Api(app)

csvfile = open('daily.csv', 'r')
reader = csv.DictReader(csvfile)
json_data = json.dumps([row for row in reader])
parsed_json = json.loads(json_data)



class historical(Resource):
    def get(self):
        conn = engine.connect()
        query = conn.execute("SELECT DATE FROM dailyTb")
        print(query.cursor)
        output = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        if len(output) == 0:
            abort(404)
        else:
            return output


class someday(Resource):
    def get(self, date):
        conn = engine.connect()
        query = conn.execute("SELECT * FROM dailyTb WHERE DATE='%s'" % date)
        output = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        if len(output) == 0:
            abort(404)
        else:
            return output[0]


@app.route('/historical/', methods=['POST'])
def insert():
    requested_data = request.data
    output = json.loads(requested_data)
    #print('output')
    date = output['DATE']
    tmax = output['TMAX']
    tmin = output['TMIN']
    conn = engine.connect()
    query = conn.execute("INSERT INTO dailyTb(DATE, TMAX, TMIN) VALUES ('%s','%f','%f')" % (date, tmax, tmin))
    return make_response(jsonify({'DATE': date, 'TMAX': tmax, 'TMIN': tmin}), 201)


@app.route('/historical/<string:date>', methods=['DELETE'])
def delete(date):
    conn = engine.connect()
    query = conn.execute("DELETE FROM dailyTb WHERE DATE='%s'" % date)
    return make_response(jsonify(date), 200)


class forecast(Resource):
    def get(self, date):
        day1 = int(date)
        day7 = day1 + 6
        conn = engine.connect()
        query = conn.execute("SELECT * FROM dailyTb WHERE DATE >= %d and DATE <= %d" % (day1, day7))
        output = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        if len(output) != 7:
            for day in parsed_json['forecast']['simpleforecast']['forecastday']:
                data_day = '{:02}'.format(day['date']['day'])
                data_month = '{:02}'.format(day['date']['month'])
                data_year = day['date']['year']
                F_Tmax = day['high']['fahrenheit']
                F_Tmin = day['low']['fahrenheit']
                data_date = str(str(data_year) + str(data_month) + str(data_day))
                conn = engine.connect()
                query = conn.execute("INSERT INTO forecast_daily(DATE, TMAX, TMIN) VALUES ('%s','%f','%f')" % (
                    data_date, F_Tmax, F_Tmin))
                query_1 = conn.execute("SELECT * FROM forecast_daily")
                f_data = [dict(zip(tuple(query_1.keys()), i)) for i in query_1.cursor]
            return f_data
        else:
            return output

@app.route('/')
def index():
    return render_template('index.html')

api.add_resource(historical, '/historical/')
api.add_resource(someday, '/historical/<string:date>')
api.add_resource(forecast, '/forecast/<string:date>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8081)
