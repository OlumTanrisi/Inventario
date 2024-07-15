import mysql.connector
from mysql.connector import Error
import time

class Product:
    def __init__(self, id, date, department, type, model, unit, quantity):
        self.id = id
        self.date = date
        self.department = department
        self.type = type
        self.model = model
        self.unit = unit
        self.quantity = quantity

    def __str__(self):
        return "Product ID:{}\nDate: {}\nDepartment: {}\nType: {}\nModel: {}\nUnit: {}\nQuantity: {}".format(
            self.id, self.date, self.department, self.type, self.model, self.unit, self.quantity
        )

class Inventory:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        try:
            self.conn = mysql.connector.connect(
                host='exmplo: localhost',
                user='exemplo: root',
                password='sua senha',
                database='nome da database'
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
            unit VARCHAR(255) NOT NULL,
            quantity INT NOT NULL
        );
        """
        self.cursor.execute(query)
        self.conn.commit()

    def add_product(self, product):
        query = "INSERT INTO inventory (id, date, department, type, model, unit, quantity) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(query, (product.id, product.date, product.department, product.type, product.model, product.unit, product.quantity))
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
                print("Product ID: {}\nProduct Date: {}\nProduct Department: {}\nProduct Type: {}\nProduct Model: {}\nProduct Unit: {}\nProduct Quantity: {}\n ".format(
                    row[0], row[1], row[2], row[3], row[4], row[5], row[6]
                ))
        else:
            print("No products in the inventory")

    def update_product(self, product):
        query = "UPDATE inventory SET date = %s, department = %s, type = %s, model = %s, unit = %s, quantity = %s WHERE id = %s"
        self.cursor.execute(query, (product.date, product.department, product.type, product.model, product.unit, product.quantity, product.id))
        self.conn.commit()

    def search_product(self, id):
        query = "SELECT * FROM inventory WHERE id = %s"
        self.cursor.execute(query, (id,))
        rows = self.cursor.fetchall()
        if rows:
            for row in rows:
                print("Product ID: {}\nProduct Date: {}\nProduct Department: {}\nProduct Type: {}\nProduct Model: {}\nProduct Unit: {}\nProduct Quantity: {}\n ".format(
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
        id = input("Enter product ID: ")
        date = input("Enter product date (YYYY-MM-DD): ")
        department = input("Enter product department: ")
        type = input("Enter product type: ")
        model = input("Enter product model: ")
        unit = input("Enter product unit: ")
        quantity = int(input("Enter product quantity: "))
        new_product = Product(id, date, department, type, model, unit, quantity)

        print("{} is being added".format(id))
        time.sleep(2)
        inventory.add_product(new_product)
        print("{} is added".format(id))

    elif choice == 2:
        id = input("Enter product ID: ")

        print("{} is being removed\n".format(id))
        time.sleep(2)
        inventory.remove_product(id)
        print("{} is removed\n".format(id))

    elif choice == 3:
        print("Listing products...")
        time.sleep(2)
        inventory.list_products()
        print("Products are listed")

    elif choice == 4:
        id = input("Enter product ID to update: ")
        date = input("Enter product date to update (YYYY-MM-DD): ")
        department = input("Enter product department to update: ")
        type = input("Enter product type to update: ")
        model = input("Enter product model to update: ")
        unit = input("Enter product unit to update: ")
        quantity = int(input("Enter product quantity to update: "))
        updated_product = Product(id, date, department, type, model, unit, quantity)

        print("{} is being updated\n".format(id))
        time.sleep(2)
        inventory.update_product(updated_product)
        print("{} is updated\n".format(id))

    elif choice == 5:
        id = input("Enter product ID for searching: ") 
        print("{} is being searched\n".format(id))
        time.sleep(2)
        inventory.search_product(id)
        print("{} is listed\n".format(id))

    elif choice == 6:
        break

    else:
        print("Invalid choice")

