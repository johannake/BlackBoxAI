import sqlite3
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI(title="Federated Learning Data Provider", version="2.1")
security = HTTPBearer()

DB_FILE = "datasharing.db"

def init_db():
    """Initializes the SQLite database and seeds initial test data if empty."""
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

    # Seed initial tokens if table is empty
    cursor.execute("SELECT COUNT(*) FROM tokens")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO tokens VALUES ('token-logistics', 'Logistics Partner Ltd', 'basic')")
        cursor.execute("INSERT INTO tokens VALUES ('token-admin', 'Admin Corp', 'advanced')")

    # Seed initial shared data if table is empty
    cursor.execute("SELECT COUNT(*) FROM shared_data")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO shared_data (item, quantity, required_access) VALUES ('Sensor Unit', 1420, 'basic')")
        cursor.execute("INSERT INTO shared_data (item, quantity, required_access) VALUES ('Spare Parts Package A', 300, 'basic')")
        cursor.execute("INSERT INTO shared_data (item, quantity, required_access) VALUES ('Secret Prototype Chip', 50, 'advanced')")
        cursor.execute("INSERT INTO shared_data (item, quantity, required_access) VALUES ('Exact Factory Energy Consumption', 9999, 'advanced')")

    conn.commit()
    conn.close()

@app.on_event("startup")
def startup_event():
    init_db()


# 1. Vanha raakadatan jakamisen endpoint (säilytetään vertailun vuoksi)
@app.get("/api/v1/shared-data")
def get_shared_data(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT consumer_name, access_level FROM tokens WHERE token = ?", (token,))
    result = cursor.fetchone()
    if not result:
        conn.close()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or unknown token.")
    
    consumer_name, access_level = result
    
    if access_level == "advanced":
        cursor.execute("SELECT item, quantity, required_access FROM shared_data")
    else:
        cursor.execute("SELECT item, quantity, required_access FROM shared_data WHERE required_access = 'basic'")
        
    rows = cursor.fetchall()
    conn.close()
    
    return {
        "status": "success",
        "provider": "Manufacturing Plant Ltd",
        "authorized_for": consumer_name,
        "payload": [{"item": r[0], "quantity": r[1], "classification": r[2]} for r in rows]
    }


# 2. UUSI FEDERATED LEARNING -ENDPOINT (Palauttaa vain mallin painot, ei raakadataa!)
@app.get("/api/v1/model-weights")
def get_model_weights(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Authenticate consumer
    cursor.execute("SELECT consumer_name, access_level FROM tokens WHERE token = ?", (token,))
    result = cursor.fetchone()
    
    if not result:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or unknown token."
        )
        
    consumer_name, access_level = result
    
    # Check how many local data rows this provider has (used as sample size for FL weighting)
    cursor.execute("SELECT COUNT(*) FROM shared_data")
    sample_size = cursor.fetchone()[0]
    conn.close()
    
    # Simulate local machine learning training on the local database:
    # Instead of exposing raw rows, the plant trains a model locally and shares only weights.
    simulated_weights = [0.452, -0.128, 0.891]
    
    return {
        "status": "success",
        "provider": "Manufacturing Plant Ltd",
        "coordinator": consumer_name,
        "access_level": access_level,
        "sample_size": sample_size,
        "model_weights": simulated_weights,
        "privacy_guarantee": "100% Data Sovereignty - Raw data never left the provider."
    }