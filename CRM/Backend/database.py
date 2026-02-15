import os
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()

db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "3306"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "database": os.getenv("DB_NAME", "crm_db")
}

try:
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="crm_pool",
        pool_size=5,
        **db_config
    )
except mysql.connector.Error as err:
    print(f"Error creating connection pool: {err}")
    connection_pool = None

def get_db_connection():
    if connection_pool:
        return connection_pool.get_connection()
    return None

def call_stored_procedure(proc_name, args=()):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.callproc(proc_name, args)
        
        results = []
        for result in cursor.stored_results():
            results.extend(result.fetchall())
            
        conn.commit()
        return results
    except mysql.connector.Error as err:
        print(f"Error calling procedure {proc_name}: {err}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def execute_query(query, params=(), fetch=False):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        if fetch:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = cursor.rowcount
        return result
    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def log_email(lead_id, sender, recipient, subject, body, direction):
    query = """
    INSERT INTO emails (lead_id, sender, recipient, subject, body, direction)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    return execute_query(query, (lead_id, sender, recipient, subject, body, direction))

def get_lead_emails(lead_id):
    query = "SELECT * FROM emails WHERE lead_id = %s ORDER BY sent_at ASC"
    return execute_query(query, (lead_id,), fetch=True)

def get_lead_by_id(lead_id):
    query = "SELECT * FROM leads WHERE lead_id = %s"
    results = execute_query(query, (lead_id,), fetch=True)
    return results[0] if results else None
