import sqlite3
import os
import openai
import getpass
import streamlit as st
from langchain.utilities import SQLDatabase
from langchain.llms import OpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.utilities import SQLDatabase
from langchain_openai import OpenAI
from langchain.agents import create_sql_agent
import os
from dotenv import load_dotenv
import subprocess
import sys
from dotenv import load_dotenv
database_file_path = './sql_lite_database.db'

# Check if database file exists and delete if it does
if os.path.exists(database_file_path):
    os.remove(database_file_path)
    message = "File 'sql_lite_database.db' found and deleted."
else:
    message = "File 'sql_lite_database.db' does not exist."

# Step 1: Connect to the database or create it if it doesn't exist
conn = sqlite3.connect(database_file_path)

# Step 2: Create a cursor
cursor = conn.cursor()

# Step 3: Create tables
create_table_query1 = """
                        CREATE TABLE Suppliers (
                                id INT PRIMARY KEY,
                                name VARCHAR(100),
                                address VARCHAR(255),
                                contact VARCHAR(20)
                        );
                        """

create_table_query2 = """
                        CREATE TABLE Products (
                                id INT PRIMARY KEY,
                                name VARCHAR(100),
                                description TEXT,
                                price DECIMAL(10, 2),
                                supplier_id INT,
                                FOREIGN KEY (supplier_id) REFERENCES Suppliers(id)
                            );
                        """

create_table_query3 = """
                        CREATE TABLE Inventory (
                                product_id INT,
                                quantity INT,
                                min_required INT,
                                PRIMARY KEY (product_id),
                                FOREIGN KEY (product_id) REFERENCES Products(id)
                        );
                        """

queries = [create_table_query1, create_table_query2, create_table_query3]

for query in queries:
    cursor.execute(query)

sql_suppliers = [
    "INSERT INTO Suppliers (id, name, address, contact) VALUES (1, 'Samsung Electronics', 'Seoul, South Korea', '800-726-7864')",
    "INSERT INTO Suppliers (id, name, address, contact) VALUES (2, 'Apple Inc.', 'Cupertino, California, USA', '800–692–7753')",
    "INSERT INTO Suppliers (id, name, address, contact) VALUES (3, 'OnePlus Technology', 'Shenzhen, Guangdong, China', '400-888-1111')",
    "INSERT INTO Suppliers (id, name, address, contact) VALUES (4, 'Google LLC', 'Mountain View, California, USA', '855-836-3987')",
    "INSERT INTO Suppliers (id, name, address, contact) VALUES (5, 'Xiaomi Corporation', 'Beijing, China', '1800-103-6286')"
]

# SQL statements for Products
sql_products = [
    "INSERT INTO Products (id, name, description, price, supplier_id) VALUES (1, 'Samsung Galaxy S21', 'Samsung flagship smartphone', 799.99, 1)",
    "INSERT INTO Products (id, name, description, price, supplier_id) VALUES (2, 'Samsung Galaxy Note 20', 'Samsung premium smartphone with stylus', 999.99, 1)",
    "INSERT INTO Products (id, name, description, price, supplier_id) VALUES (3, 'iPhone 13 Pro', 'Apple flagship smartphone', 999.99, 2)",
    "INSERT INTO Products (id, name, description, price, supplier_id) VALUES (4, 'iPhone SE', 'Apple budget smartphone', 399.99, 2)",
    "INSERT INTO Products (id, name, description, price, supplier_id) VALUES (5, 'OnePlus 9', 'High performance smartphone', 729.00, 3)",
    "INSERT INTO Products (id, name, description, price, supplier_id) VALUES (6, 'OnePlus Nord', 'Mid-range smartphone', 499.00, 3)",
    "INSERT INTO Products (id, name, description, price, supplier_id) VALUES (7, 'Google Pixel 6', 'Google''s latest smartphone', 599.00, 4)",
    "INSERT INTO Products (id, name, description, price, supplier_id) VALUES (8, 'Google Pixel 5a', 'Affordable Google smartphone', 449.00, 4)",
    "INSERT INTO Products (id, name, description, price, supplier_id) VALUES (9, 'Xiaomi Mi 11', 'Xiaomi high-end smartphone', 749.99, 5)",
    "INSERT INTO Products (id, name, description, price, supplier_id) VALUES (10, 'Xiaomi Redmi Note 10', 'Xiaomi budget smartphone', 199.99, 5)"
]


# SQL statements for Inventory
sql_inventory = [
    "INSERT INTO Inventory (product_id, quantity, min_required) VALUES (1, 150, 30)",
    "INSERT INTO Inventory (product_id, quantity, min_required) VALUES (2, 100, 20)",
    "INSERT INTO Inventory (product_id, quantity, min_required) VALUES (3, 120, 30)",
    "INSERT INTO Inventory (product_id, quantity, min_required) VALUES (4, 80, 15)",
    "INSERT INTO Inventory (product_id, quantity, min_required) VALUES (5, 200, 40)",
    "INSERT INTO Inventory (product_id, quantity, min_required) VALUES (6, 150, 25)",
    "INSERT INTO Inventory (product_id, quantity, min_required) VALUES (7, 100, 20)",
    "INSERT INTO Inventory (product_id, quantity, min_required) VALUES (8, 90, 18)",
    "INSERT INTO Inventory (product_id, quantity, min_required) VALUES (9, 170, 35)",
    "INSERT INTO Inventory (product_id, quantity, min_required) VALUES (10, 220, 45)"
]

# Execute SQL statements for Suppliers
for query in sql_suppliers:
    cursor.execute(query)

# Execute SQL statements for Products
for query in sql_products:
    cursor.execute(query)

# Execute SQL statements for Inventory
for query in sql_inventory:
    cursor.execute(query)
# Step 7: Close the cursor and connection
cursor.close()
conn.commit()
conn.close()
db = SQLDatabase.from_uri('sqlite:///sql_lite_database.db')
def main():
    st.title("SQL Agent Web App")
    prompt = st.text_input("Ask a question:")
    if st.button("Ask"):
        st.write(agent_executor.invoke(prompt))

try:
    st.title("Streamlit SQL Query App")
    api_key_placeholder = st.empty()  # Create an empty placeholder
    api_key = api_key_placeholder.text_input("Enter your OpenAI API Key:", type="password")
    os.environ['OPENAI_API_KEY'] = api_key
    load_dotenv()
# choose llm model, in this case the default OpenAI model
    llm = OpenAI(
            temperature=0,
            verbose=True,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            )
# setup agent
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)
    st.empty()
    api_key_placeholder.empty()
    main()
except:
    st.write("invalid api [-_-] try again :<")
