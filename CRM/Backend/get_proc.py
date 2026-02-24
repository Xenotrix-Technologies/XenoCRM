import database

def get_proc():
    try:
        results = database.execute_query("SHOW CREATE PROCEDURE InsertMetaLead;", fetch=True)
        if results:
            print(results[0]['Create Procedure'])
        else:
            print("Procedure not found")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_proc()
