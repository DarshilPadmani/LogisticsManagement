import streamlit as st
import pandas as pd
import mysql.connector

# Define the function to connect to the MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Dars@123",
        database="logisticsmanagement"
    )

# Define functions to create tables, insert, delete, update, and view data
def create_tables():
    conn = connect_to_database()
    cursor = conn.cursor()
    # Create tables if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS Customers(
                        customer_id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        address VARCHAR(255),
                        contact_info VARCHAR(255)
                        )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Warehouses (
                        warehouse_id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        location VARCHAR(255),
                        capacity INT
                        )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Employees (
                        employee_id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        position VARCHAR(255),
                        department VARCHAR(255),
                        contact_info VARCHAR(255)
                        )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Vehicles (
                        vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
                        type VARCHAR(255),
                        capacity INT,
                        status VARCHAR(255)
                        )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Shipments (
                        shipment_id INT AUTO_INCREMENT PRIMARY KEY,
                        sender_id INT,
                        receiver_id INT,
                        origin_warehouse_id INT,
                        destination_warehouse_id INT,
                        departure_time DATETIME,
                        arrival_time DATETIME,
                        status VARCHAR(255),
                        FOREIGN KEY (sender_id) REFERENCES Customers(customer_id),
                        FOREIGN KEY (receiver_id) REFERENCES Customers(customer_id),
                        FOREIGN KEY (origin_warehouse_id) REFERENCES Warehouses(warehouse_id),
                        FOREIGN KEY (destination_warehouse_id) REFERENCES Warehouses(warehouse_id)
                        )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Routes (
                        route_id INT AUTO_INCREMENT PRIMARY KEY,
                        origin_location VARCHAR(255),
                        destination_location VARCHAR(255),
                        distance FLOAT,
                        duration INT
                        )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Orders (
                        order_id INT AUTO_INCREMENT PRIMARY KEY,
                        customer_id INT,
                        shipment_id INT,
                        order_date DATE,
                        delivery_date DATE,
                        status VARCHAR(255),
                        FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
                        FOREIGN KEY (shipment_id) REFERENCES Shipments(shipment_id)
                        )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Inventory (
                        inventory_id INT AUTO_INCREMENT PRIMARY KEY,
                        warehouse_id INT,
                        product_id INT,
                        quantity INT,
                        FOREIGN KEY (warehouse_id) REFERENCES Warehouses(warehouse_id)
                        )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Products (
                        product_id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255),
                        description TEXT,
                        price DECIMAL(10, 2)
                        )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Routes_Vehicles (
                        route_id INT,
                        vehicle_id INT,
                        PRIMARY KEY (route_id, vehicle_id),
                        FOREIGN KEY (route_id) REFERENCES Routes(route_id),
                        FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id)
                        )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Employees_Shipments (
                        employee_id INT,
                        shipment_id INT,
                        role VARCHAR(255),
                        PRIMARY KEY (employee_id, shipment_id),
                        FOREIGN KEY (employee_id) REFERENCES Employees(employee_id),
                        FOREIGN KEY (shipment_id) REFERENCES Shipments(shipment_id)
                        )''')

    conn.commit()
    cursor.close()
    conn.close()
    st.write('Tables created successfully')

# Define CRUD functions
def insert_data(table_name, args):
    conn = connect_to_database()
    cursor = conn.cursor()
    columns = ', '.join(args.keys())
    placeholders = ', '.join(['%s'] * len(args))
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, list(args.values()))
    conn.commit()
    cursor.close()
    conn.close()

# def delete_data(table_name, primary_key):
#     conn = connect_to_database()
#     cursor = conn.cursor()
#     sql = f"DELETE FROM {table_name} WHERE {table_name[:-1]}_id = %s"
#     cursor.execute(sql, (primary_key,))
#     conn.commit()
#     cursor.close()
#     conn.close()


def update_data(table_name, primary_key, args):
    conn = connect_to_database()
    cursor = conn.cursor()
    set_statement = ', '.join([f"{key} = %s" for key in args.keys()])
    sql = f"UPDATE {table_name} SET {set_statement} WHERE {table_name[:-1]}_id = %s"
    cursor.execute(sql, list(args.values()) + [primary_key])
    conn.commit()
    cursor.close()
    conn.close()

def view_data(table_name):
    conn = connect_to_database()
    cursor = conn.cursor()
    sql = f"SELECT * FROM {table_name}"
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def get_table_columns(table_name):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    columns = [col[0] for col in cursor.fetchall()]
    cursor.close()
    conn.close()
    return columns

# Define the main function
def main():
    st.title("Logistics Management System")
    create_tables()

    menu = ["Insert Data", "Delete Data", "Update Data", "View Data"]
    choice = st.sidebar.selectbox("Select Option", menu)

    if choice == "Insert Data":
        st.subheader("Insert Data")
        table_name = st.selectbox("Select Table", ["Customers", "Warehouses", "Employees", "Vehicles", "Shipments", "Routes", "Orders", "Inventory", "Products", "Routes_Vehicles", "Employees_Shipments"])
        if table_name:
            columns = get_table_columns(table_name)
            args = {}
            for column in columns:
                args[column] = st.text_input(column)
            if st.button("Insert"):
                insert_data(table_name, args)
                st.success(f"{table_name} Data Inserted Successfully!")

    elif choice == "Delete Data":
        st.subheader("Delete Data")
        table_name = st.selectbox("Select Table", ["Customers", "Warehouses", "Employees", "Vehicles", "Shipments", "Routes", "Orders", "Inventory", "Products", "Routes_Vehicles", "Employees_Shipments"])
        primary_key = st.text_input(f"Enter {table_name.lower()}_id to delete")
        if primary_key and st.button("Delete"):
            delete_data(table_name, primary_key)
            st.success(f"{table_name} Data Deleted Successfully!")

    elif choice == "Update Data":
        st.subheader("Update Data")
        table_name = st.selectbox("Select Table", ["Customers", "Warehouses", "Employees", "Vehicles", "Shipments", "Routes", "Orders", "Inventory", "Products", "Routes_Vehicles", "Employees_Shipments"])
        primary_key = st.text_input(f"Enter {table_name.lower()}_id to update")
        if primary_key:
            columns = get_table_columns(table_name)
            args = {}
            for column in columns:
                args[column] = st.text_input(column)
            if st.button("Update"):
                update_data(table_name, primary_key, args)
                st.success(f"{table_name} Data Updated Successfully!")

    elif choice == "View Data":
        st.subheader("View Data")
        table_name = st.selectbox("Select Table", ["Customers", "Warehouses", "Employees", "Vehicles", "Shipments", "Routes", "Orders", "Inventory", "Products", "Routes_Vehicles", "Employees_Shipments"])
        if table_name:
            data = view_data(table_name)
            df = pd.DataFrame(data, columns=get_table_columns(table_name))
            st.dataframe(df)

if __name__ == "__main__":
    main()

