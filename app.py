from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['smart_city']
sensors_collection = db['sensors_data']

@app.route('/data', methods=['POST'])
def add_data():
    data = request.json
    data['timestamp'] = datetime.now()
    sensors_collection.insert_one(data)
    return jsonify({'msg': 'Data added'}), 201

@app.route('/data/<sensor_type>', methods=['GET'])
def get_data(sensor_type):
    data = list(sensors_collection.find({'type': sensor_type}, {'_id': 0}))
    return jsonify(data)

@app.route('/data/latest/<sensor_type>', methods=['GET'])
def get_latest_data(sensor_type):
    data = sensors_collection.find({'type': sensor_type}, {'_id': 0}).sort('timestamp', -1).limit(1)
    return jsonify(data[0]) if data else jsonify({'msg': 'No data found'})

if __name__ == '__main__':
    app.run(debug=True)
