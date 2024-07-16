import mysql.connector
from mysql.connector import Error
import time

class Product:
    def __init__(self, id, date, department, type, model, value_unit, with_user):
        self.id = id
        self.date = date
        self.department = department
        self.type = type
        self.model = model
        self.value_unit = value_unit
        self.with_user = with_user

    def __str__(self):
        return "Product ID:{}\nDate: {}\nDepartment: {}\nType: {}\nModel: {}\nValue_Unit: {}\nWith User: {}".format(
            self.id, self.date, self.department, self.type, self.model, self.value_unit, self.with_user
        )

class Inventory:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        try:
            self.conn = mysql.connector.connect(
                host='host',
                user='user',
                password='password',
                database='name'
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
            with_user VARCHAR(255) NOT NULL
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

    def add_product(self, product):
        product.id = self.get_next_id()
        query = "INSERT INTO inventory (id, date, department, type, model, value_unit, with_user) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(query, (product.id, product.date, product.department, product.type, product.model, product.value_unit, product.with_user))
        self.conn.commit()

    def remove_product(self, id):
        query = "DELETE FROM inventory WHERE id = %s"
        self.cursor.execute(query, (id,))
        self.conn.commit()

    def list_products(self):
        query = "SELECT * FROM inventory"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        if rows:
            for row in rows:
                print("Product ID: {}\nProduct Date: {}\nProduct Department: {}\nProduct Type: {}\nProduct Model: {}\nProduct Value Unit: {}\nProduct With User: {}\n ".format(
                    row[0], row[1], row[2], row[3], row[4], row[5], row[6]
                ))
        else:
            print("No products in the inventory")

    def update_product(self, product):
        query = "UPDATE inventory SET date = %s, department = %s, with_user = %s WHERE id = %s"
        self.cursor.execute(query, (product.date, product.department, product.with_user, product.id))
        self.conn.commit()

    def search_product(self, id):
        query = "SELECT * FROM inventory WHERE id = %s"
        self.cursor.execute(query, (id,))
        rows = self.cursor.fetchall()
        if rows:
            for row in rows:
                print("Product ID: {}\nProduct Date: {}\nProduct Department: {}\nProduct Type: {}\nProduct Model: {}\nProduct Unit: {}\nProduct With User: {}\n ".format(
                    row[0], row[1], row[2], row[3], row[4], row[5], row[6]
                ))
        else:
            print("Product not found")

# Example of usage
print(""" 
1. Add product 
2. Remove product
3. List All Products
4. Update Product
5. Search Product
6. Exit
""")

inventory = Inventory()

while True:
    choice = int(input("Enter your choice: "))
    
    if choice == 1:
        date = input("Enter product date (YYYY-MM-DD): ")
        department = input("Enter product department: ")
        type = input("Enter product type: ")
        model = input("Enter product model: ")
        value_unit = input("Enter product value unit: ")
        with_user = input("Enter product with user: ")
        
        new_product = Product(None, date, department, type, model, value_unit, with_user)

        print("Adding product...")
        time.sleep(2)
        inventory.add_product(new_product)
        print("Product added with ID:", new_product.id)

    elif choice == 2:
        id = input("Enter product ID: ")

        print("Removing product...")
        time.sleep(2)
        inventory.remove_product(id)
        print("Product removed")

    elif choice == 3:
        print("Listing products...")
        time.sleep(2)
        inventory.list_products()
        print("Products listed")

    elif choice == 4:
        id = input("Enter product ID to update: ")
        date = input("Enter product date to update (YYYY-MM-DD): ")
        department = input("Enter product department to update: ")
        with_user = input("Enter product with user to update: ")

        updated_product = Product(id, date, department, None, None, None, with_user)

        print("Updating product...")
        time.sleep(2)
        inventory.update_product(updated_product)
        print("Product updated")

    elif choice == 5:
        id = input("Enter product ID for searching: ") 
        print("Searching product...")
        time.sleep(2)
        inventory.search_product(id)
        print("Product search completed")

    elif choice == 6:
        break

    else:
        print("Invalid choice")
