import json
from flask import Flask, jsonify, request
app = Flask(__name__)

products = [
 { 'id': 1, 'name': 'T-shirt' },
 { 'id': 2, 'name': 'Shirt' },
 { 'id': 3, 'name': 'kurthi' }
]


nextProductId = 4
3
@app.route('/products', methods=['GET'])
def get_products():
 return jsonify(products)

@app.route('/products/<int:id>', methods=['GET'])
def get_products_by_id(id: int):
 products = get_products(id)
 if products is None:
   return jsonify({ 'error': 'Product does not exist'}), 404
 return jsonify(products)

def get_products(id):
 return next((e for e in products if e['id'] == id), None)

def products_is_valid(products):
 for key in products.keys():
   if key != 'name':
        return False
 return True

@app.route('/products', methods=['POST'])
def create_products():
 global nextProductId
 products = json.loads(request.data)
 if not products_is_valid(products):
   return jsonify({ 'error': 'Invalid products properties.' }), 400

 products['id'] = nextProductId
 nextProductId += 1
 products.append(products)

 return '', 201, { 'location': f'/products/{products["id"]}' }

@app.route('/products/<int:id>', methods=['PUT'])
def update_products(id: int):
 products = get_products(id)
 if products is None:
   return jsonify({ 'error': 'Product does not exist.' }), 404

 updated_products = json.loads(request.data)
 if not products_is_valid(updated_products):
   return jsonify({ 'error': 'Invalid products properties.' }), 400

 products.update(updated_products)

 return jsonify(products)

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_products(id: int):
 global products
 products = get_products(id)
 if products is None:
   return jsonify({ 'error': 'Products does not exist.' }), 404

 products = [e for e in products if e['id'] != id]
 return jsonify(products), 200

if __name__ == '__main__':
   app.run(port=5000)