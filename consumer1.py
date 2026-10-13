import requests

URL = "http://127.0.0.1:8000/api/v1/shared-data"

# Choose either 'token-logistics' or 'token-admin'
TOKEN = "token-admin" 

headers = {"Authorization": f"Bearer {TOKEN}"}

def fetch_data():
    try:
        print("Contacting the data provider...")
        response = requests.get(URL, headers=headers)
        if response.status_code == 200:
            print("\n[OK] Data fetch successful!")
            data = response.json()
            print(f"Company: {data['authorized_for']} (Access Level: {data['access_level']})")
            print("Received Data:")
            for item in data['payload']:
                print(f" - {item['item']}: {item['quantity']} pcs (Classification: {item['classification']})")
        else:
            print(f"\n[ERROR]: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Connection failed. Is provider.py running?")

if __name__ == "__main__":
    fetch_data()