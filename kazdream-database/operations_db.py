import sqlite3 as sq
import json
import os





def insert_into_table(data_json, table_name):
    with sq.connect('shopkz.db') as conn:
        cur = conn.cursor()

        cur.execute(f'''CREATE TABLE IF NOT EXISTS {table_name}
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    articul TEXT NOT NULL,
                    price TEXT NOT NULL DEFAULT "Нет в наличии",
                    description TEXT NOT NULL,
                    photo_urls TEXT NOT NULL);''')        

        for k, v in data_json.items():
            for k2, v2 in v.items():
                cur.execute(
                    f"INSERT INTO {table_name} (name, articul, price, description, photo_urls) VALUES (?, ?, ?, ?, ?)", 
                    (v2['name'], v2['articul'], v2['price'], v2['description'], v2['photo_urls']))
        
    print('[db] insertion successful')





