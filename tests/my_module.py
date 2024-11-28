import requests

def fetch_data(url):
    """Fetch data from a URL."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f"Error fetching data: {response.status_code}")