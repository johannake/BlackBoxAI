import os
import sqlite3

# Define separate databases for two different factories/plants
DB_PLANT_A = "plant_a.db"
DB_PLANT_B = "plant_b.db"

def setup_mock_factories():
    """Creates two separate databases to simulate two different companies/plants."""
    
    # Plant A data
    if os.path.exists(DB_PLANT_A):
        os.remove(DB_PLANT_A)
    conn_a = sqlite3.connect(DB_PLANT_A)
    cursor_a = conn_a.cursor()
    cursor_a.execute("CREATE TABLE metrics (item TEXT, quantity INTEGER)")
    cursor_a.executemany("INSERT INTO metrics VALUES (?, ?)", [
        ("Sensor Unit", 1420),
        ("Spare Parts Package A", 300)
    ])
    conn_a.commit()
    conn_a.close()

    # Plant B data
    if os.path.exists(DB_PLANT_B):
        os.remove(DB_PLANT_B)
    conn_b = sqlite3.connect(DB_PLANT_B)
    cursor_b = conn_b.cursor()
    cursor_b.execute("CREATE TABLE metrics (item TEXT, quantity INTEGER)")
    cursor_b.executemany("INSERT INTO metrics VALUES (?, ?)", [
        ("Secret Prototype Chip", 50),
        ("Factory Energy Consumption", 9999)
    ])
    conn_b.commit()
    conn_b.close()

def local_factory_computation(db_file, factory_name):
    """
    Simulates local computation at a plant. 
    The plant keeps its raw data strictly internal and calculates only 
    the necessary summary (sum and count).
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Fetch raw data from the plant's own database
    cursor.execute("SELECT item, quantity FROM metrics")
    raw_data = cursor.fetchall()
    conn.close()

    # Local computation (simulates local model training)
    quantities = [row[1] for row in raw_data]
    local_sum = sum(quantities)
    local_count = len(quantities)

    print(f"\n--- {factory_name} ---")
    print(f"  [Secret raw data at plant]: {raw_data}")
    print(f"  [Locally calculated sum]: {local_sum}")
    print(f"  [Local sample size]: {local_count} items")
    print(f"  -> Sending forward ONLY the sum and sample size (raw data stays internal).")

    return local_sum, local_count

def run_federated_demo():
    print("=== FEDERATED LEARNING / DISTRIBUTED COMPUTING DEMO ===")
    print("Goal: Calculate a joint average across companies without exposing raw data.")
    
    # 1. Initialize separate databases
    setup_mock_factories()

    # 2. Plants perform computation on their own side
    sum_a, count_a = local_factory_computation(DB_PLANT_A, "Plant A (Provider 1)")
    sum_b, count_b = local_factory_computation(DB_PLANT_B, "Plant B (Provider 2)")

    # 3. Consumer / Coordinator aggregates the results (Federated Averaging)
    total_sum = sum_a + sum_b
    total_count = count_a + count_b
    global_average = total_sum / total_count

    print("\n" + "=" * 50)
    print("[Consumer / Coordinator] Aggregates results:")
    print(f"  - Total items processed: {total_count} pcs")
    print(f"  - Grand total sum: {total_sum}")
    print(f"  ==> GLOBAL AVERAGE (Global Metric): {global_average}")
    print("=" * 50)
    print("\nThe result is a fully understandable business metric, even though")
    print("neither plant shared their proprietary product details or figures with each other!")

if __name__ == "__main__":
    run_federated_demo()