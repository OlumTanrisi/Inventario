from flask import Flask, request, jsonify, send_from_directory, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

class Product:
    def __init__(self, id, date, department, type, model, value_unit, with_user, description, quality):
        self.id = id
        self.date = date
        self.department = department
        self.type = type
        self.model = model
        self.value_unit = value_unit
        self.with_user = with_user
        self.description = description
        self.quality = quality

class Inventory:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='admin',
                database='inventory'
            )
            if self.conn.is_connected():
                self.cursor = self.conn.cursor()
                print("Connection established")
        except Error as e:
            print(f"Error: {e}")

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS inventory (
            id VARCHAR(255) PRIMARY KEY,
            date DATE NOT NULL,
            department VARCHAR(255) NOT NULL,
            type VARCHAR(255) NOT NULL,
            model VARCHAR(255) NOT NULL,
            value_unit VARCHAR(255) NOT NULL,
            with_user VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL,
            quality VARCHAR(10) NOT NULL
        );
        """
        self.cursor.execute(query)
        self.conn.commit()

    def get_next_id(self):
        query = "SELECT id FROM inventory ORDER BY id DESC LIMIT 1"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result:
            last_id = result[0]
            prefix, num = last_id.split('-')
            next_num = int(num) + 1
            next_id = f"{prefix}-{next_num:05d}"
        else:
            next_id = "EQP-00001"
        return next_id

    def add_product(self, product, quantity=1):
        next_id = self.get_next_id()
        for _ in range(quantity):
            product.id = next_id
            query = "INSERT INTO inventory (id, date, department, type, model, value_unit, with_user, description, quality) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(query, (product.id, product.date, product.department, product.type, product.model, product.value_unit, product.with_user, product.description, product.quality))
            self.conn.commit()
            next_id = self.increment_id(next_id)

    def increment_id(self, current_id):
        prefix, num = current_id.split('-')
        next_num = int(num) + 1
        return f"{prefix}-{next_num:05d}"

    def remove_product(self, id):
        query = "DELETE FROM inventory WHERE id = %s"
        self.cursor.execute(query, (id,))
        self.conn.commit()

    def list_products(self):
        query = "SELECT * FROM inventory"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        products = []
        if rows:
            for row in rows:
                product = {
                    "id": row[0],
                    "date": row[1],
                    "department": row[2],
                    "type": row[3],
                    "model": row[4],
                    "value_unit": row[5],
                    "with_user": row[6],
                    "description": row[7],
                    "quality": row[8]
                }
                products.append(product)
        return products

    def update_product(self, product):
        query = "UPDATE inventory SET date = %s, department = %s, with_user = %s, description = %s, quality = %s WHERE id = %s"
        self.cursor.execute(query, (product.date, product.department, product.with_user, product.description, product.quality, product.id))
        self.conn.commit()

    def search_product(self, id):
        query = "SELECT * FROM inventory WHERE id = %s"
        self.cursor.execute(query, (id,))
        row = self.cursor.fetchone()
        if row:
            product = {
                "id": row[0],
                "date": row[1],
                "department": row[2],
                "type": row[3],
                "model": row[4],
                "value_unit": row[5],
                "with_user": row[6],
                "description": row[7],
                "quality": row[8]
            }
            return product
        return None

inventory = Inventory()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.json
    product = Product(None, data['date'], data['department'], data['type'], data['model'], data['value_unit'], data['with_user'], data['description'], data['quality'])
    quantity = int(data['quantity'])  # Convert quantity to integer
    inventory.add_product(product, quantity)
    return jsonify({"message": "Products added successfully"})

@app.route('/remove_product', methods=['DELETE'])
def remove_product():
    id = request.json['id']
    inventory.remove_product(id)
    return jsonify({"message": "Product removed successfully"})

@app.route('/list_products', methods=['GET'])
def list_products():
    products = inventory.list_products()
    return jsonify(products)

@app.route('/update_product', methods=['PUT'])
def update_product():
    data = request.json
    product = Product(data['id'], data['date'], data['department'], None, None, None, data['with_user'], data['description'], data['quality'])
    inventory.update_product(product)
    return jsonify({"message": "Product updated successfully"})

@app.route('/search_product', methods=['GET'])
def search_product():
    id = request.args.get('id')
    product = inventory.search_product(id)
    if product:
        return jsonify(product)
    return jsonify({"message": "Product not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
