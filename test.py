import requests
import json

# Replace with the district you want to test
district = "Patna"

url = "https://efarm.digitalgreen.org/agri_mcp"
payload = {
    "state": "bihar",
    "district": district
}

headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    response.raise_for_status()

    data = response.json()
    print("Response JSON:")
    print(json.dumps(data, indent=2))

    # If CSV data is available, save it
    if 'csv' in data and data['csv']:
        filename = f"{district.lower()}-workflow.csv"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(data['csv'])
        print(f"\nCSV data saved to '{filename}'")

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
