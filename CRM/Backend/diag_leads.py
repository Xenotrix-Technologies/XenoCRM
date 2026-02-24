import database

def test():
    print("Connecting to DB...")
    conn = database.get_db_connection()
    if conn:
        print("Connected!")
        try:
            cursor = conn.cursor(dictionary=True)
            print("Querying leads...")
            cursor.execute("SELECT COUNT(*) as count FROM leads")
            result = cursor.fetchone()
            print(f"Lead Count: {result['count']}")
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Query failed: {e}")
    else:
        print("Connection failed!")

if __name__ == "__main__":
    test()
