import requests

# Point to the new Federated Learning weights endpoint
URL = "http://127.0.0.1:8000/api/v1/model-weights"

# Choose either 'token-logistics' or 'token-admin'
TOKEN = "token-admin" 

headers = {"Authorization": f"Bearer {TOKEN}"}

def fetch_federated_weights():
    try:
        print("Contacting data provider for local model weights (Federated Learning)...")
        response = requests.get(URL, headers=headers)
        
        if response.status_code == 200:
            print("\n[OK] Model weights successfully retrieved!")
            data = response.json()
            
            print(f"Coordinator: {data['coordinator']}")
            print(f"Provider: {data['provider']}")
            print(f"Local Sample Size: {data['sample_size']} records")
            print(f"Received Model Weights: {data['model_weights']}")
            print(f"Privacy Status: {data['privacy_guarantee']}")
            
            print("\n[INFO] Next step in FL: Coordinator aggregates these weights with other nodes.")
        else:
            print(f"\n[ERROR]: {response.json()}")
            
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Connection failed. Is provider.py running?")

if __name__ == "__main__":
    fetch_federated_weights()