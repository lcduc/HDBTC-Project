import pymysql
import os

DB_HOST = os.getenv("DB_HOST", "mysql-container")
DB_PORT = int(os.environ.get("DB_PORT", 3306))
DB_USER = os.environ.get("DB_USER", "admin")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "Binhlol707")
DB_NAME = os.environ.get("DB_NAME", "Greenhouse")

print(f"[DEBUG] Connecting to MySQL at {DB_HOST}:{DB_PORT} as {DB_USER} to DB {DB_NAME}")

print("?? Debug Info:")
print(f"DB_HOST={DB_HOST}")
print(f"DB_PORT={DB_PORT}")
print(f"DB_USER={DB_USER}")
print(f"DB_NAME={DB_NAME}")

try:
    connection = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM greenhouse")
    count = cursor.fetchone()[0]
    print(f"? Greenhouse count: {count}")
    
    cursor.execute("SELECT * FROM greenhouse")
    results = cursor.fetchall()
    for row in results:
        print(row)
    
    cursor.close()
    connection.close()
except Exception as e:
    print(f"? Error connecting to MySQL: {e}")
