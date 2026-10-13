import sqlite3
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI(title="Data Sharing with SQLite", version="2.0")
security = HTTPBearer()

DB_FILE = "datasharing.db"

def init_db():
    """Initializes the database and seeds test data if tables are empty."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Table for consumer tokens and access levels
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            token TEXT PRIMARY KEY,
            consumer_name TEXT,
            access_level TEXT
        )
    """)
    
    # Table for shared data items
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shared_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT,
            quantity INTEGER,
            required_access TEXT
        )
    """)
    
    # Seed initial data if tokens table is empty
    cursor.execute("SELECT COUNT(*) FROM tokens")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO tokens VALUES ('token-logistics', 'Logistics Partner Ltd', 'basic')")
        cursor.execute("INSERT INTO tokens VALUES ('token-admin', 'Admin Corp', 'advanced')")
        
    cursor.execute("SELECT COUNT(*) FROM shared_data")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO shared_data (item, quantity, required_access) VALUES ('Sensor Unit', 1420, 'basic')")
        cursor.execute("INSERT INTO shared_data (item, quantity, required_access) VALUES ('Secret Prototype Chip', 50, 'advanced')")
        
    conn.commit()
    conn.close()

# Run database initialization on startup
@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/api/v1/shared-data")
def get_shared_data(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 1. Verify token from database
    cursor.execute("SELECT consumer_name, access_level FROM tokens WHERE token = ?", (token,))
    result = cursor.fetchone()
    
    if not result:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or unknown token."
        )
        
    consumer_name, access_level = result
    
    # 2. Fetch data based on the consumer's access level
    if access_level == "advanced":
        cursor.execute("SELECT item, quantity, required_access FROM shared_data")
    else:
        # Basic users only see 'basic' level data
        cursor.execute("SELECT item, quantity, required_access FROM shared_data WHERE required_access = 'basic'")
        
    rows = cursor.fetchall()
    
    # Format database rows into a JSON-friendly structure
    data_payload = [
        {"item": row[0], "quantity": row[1], "classification": row[2]} 
        for row in rows
    ]
    
    conn.close()
    
    # 3. Return response to consumer
    return {
        "status": "success",
        "provider": "Manufacturing Plant Ltd",
        "authorized_for": consumer_name,
        "access_level": access_level,
        "payload": data_payload
    }