import database

def inspect():
    print("Tables:")
    tables = database.execute_query("SHOW TABLES;", fetch=True)
    for t in tables:
        print(t)
    
    print("\nLeads Schema:")
    schema = database.execute_query("DESCRIBE leads;", fetch=True)
    for s in schema:
        print(s)
        
    print("\nProcedures:")
    procs = database.execute_query("SHOW PROCEDURE STATUS WHERE Db = 'crm_db';", fetch=True)
    for p in procs:
        print(p['Name'])

if __name__ == "__main__":
    inspect()
