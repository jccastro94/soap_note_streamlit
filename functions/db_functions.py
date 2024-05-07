import sqlite3
import pandas as pd


def insert_data(db_path, table_name, data):
    conn = sqlite3.connect(db_path)
    columns = ', '.join(data.keys())
    placeholders = ', '.join('?' * len(data))
    sql = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
    
    try:
        cur = conn.cursor()
        cur.execute(sql, list(data.values()))
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    except Exception as e:
        print(f"Exception in _query: {e}")
        return None



def search_by_id(db_path, table, client_id):
    conn = sqlite3.connect(db_path)
    query = f"SELECT * FROM {table} WHERE id = {client_id}"
    results = pd.read_sql(query, conn)
    conn.close()
    return results
