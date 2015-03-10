import sqlite3
import json
import string
from fuzzywuzzy import fuzz
from Util import *
from DataInsertion import *

def get_product_dict(conn, cur):
    product_list = {}
    for row in cur.execute("select id, name from product_list"):
        (product_id, product) = row
        product = remove_punctuations(str(product.lower()))
        product = remove_stop_words(product)
        product_list[product] = product_id

    return product_list
    

def init_database(conn, cur):
    cur.executescript("""
        create table raw_data(
            active VARCHAR,
            thread_id INTEGER PRIMARY KEY,
            price INTEGER,
            product TEXT,
            product_id INTEGER
        );
        
        create table product_list(
            id INTEGER PRIMARY KEY,
            name TEXT,
            base_price INTEGER
        );
    
        create table buy_list(
            id INTEGER PRIMARY KEY,
            name TEXT,
            average_price INTEGER,
            num_active INTEGER,
            num_total INTEGER,
            price_diff INTEGER,
            active_product_thread INTEGER
        );
    
    """)
    
    known_abr_products = {}
    
    
    # Read in the known product list
    file_name = 'master.json'
    json_data = open(file_name)
    data = json.load(json_data)
    for entry in data:
        product = entry.items()[0][1]
        cost = entry.items()[1][1]
        insertion = 'insert into product_list(name, base_price) values ' + str('(\'') + str(product) + str('\', ') + str(cost) + str(');')
        cur.execute(insertion)
        cur.execute("select id from product_list where name = ?", (product,))
        product_id = cur.fetchone() 
    
        # Insertion into a dictionary in RAM
        product = remove_punctuations(str(product.lower()))
        product = remove_stop_words(product)
        known_abr_products[product] = product_id[0]
    
    conn.commit()
    json_data.close()
    
    raw_file = 'raw.json'
    raw_data = json.load(open(raw_file))
    unknown_product_id = known_abr_products['unknown']
    
    # Read in the raw product list
    for raw_entry in raw_data:
        active = raw_entry.items()[0][1]
        thread_id = raw_entry.items()[1][1]
        price = int(raw_entry.items()[2][1])
        product = raw_entry.items()[3][1]
    
        # Get rid of outliers
        if price < 6 or price > 9999:
            continue
        
        product_id = get_product_id(known_abr_products, product, unknown_product_id) 

        insert_raw_data(active, thread_id, price, product, product_id, cur)
    
        update_buy_list(product_id, unknown_product_id, active, thread_id, price, cur)
            
    conn.commit()
    
    return known_abr_products
    
