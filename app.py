import os
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId

MONGO_URL = 'mongodb://localhost:27017/'
DB_NAME = 'test_api_db'
COLLECTION = 'items'
PORT = 3000

app = Flask(__name__, static_folder='public', static_url_path='')
CORS(app)

client = MongoClient(MONGO_URL)
db = client[DB_NAME]
items_collection = db[COLLECTION]

@app.route('/api/items', methods=['GET'])
def get_items():
    items = list(items_collection.find())
    for item in items:
        item['_id'] = str(item['_id'])
    return jsonify(items)

@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.get_json() or {}
    name = data.get('name')
    if not name:
        return jsonify({'message': 'Name is required'}), 400

    result = items_collection.insert_one({
        'name': name,
        'createdAt': datetime.utcnow(),
    })
    return jsonify({'_id': str(result.inserted_id), 'name': name}), 201

@app.route('/api/items/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        items_collection.delete_one({'_id': ObjectId(item_id)})
        return jsonify({'message': 'Item deleted'})
    except Exception:
        return jsonify({'message': 'Invalid item id'}), 400

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    static_path = os.path.join(app.static_folder, path)
    if path and os.path.exists(static_path):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
