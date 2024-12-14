import os
import requests

# Base URL for the APIs
BASE_URL = "https://api.socialverseapp.com"
HEADERS = {
    "Flic-Token": "flic_6e2d8d25dc29a4ddd382c2383a903cf4a688d1a117f6eb43b35a1e7fadbb84b8"
}

def fetch_data(endpoint, params=None, save_path=None):
    """
    Fetches data from the given API endpoint and saves it to a file.

    Args:
        endpoint (str): The API endpoint to fetch data from.
        params (dict): Query parameters for the API request.
        save_path (str): Path to save the fetched data as a JSON file.

    Returns:
        dict: The JSON response from the API.
    """
    url = f"{BASE_URL}{endpoint}"
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code == 200:
        data = response.json()
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'w') as f:
                import json
                json.dump(data, f, indent=4)
        return data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None


def get_all_viewed_posts(page=1, page_size=1000):
    return fetch_data(
        endpoint="/posts/view",
        params={"page": page, "page_size": page_size},
        save_path=f"data/raw/viewed_posts_page_{page}.json"
    )

def get_all_liked_posts(page=1, page_size=1000):
    return fetch_data(
        endpoint="/posts/like",
        params={"page": page, "page_size": page_size},
        save_path=f"data/raw/liked_posts_page_{page}.json"
    )

def get_all_inspired_posts(page=1, page_size=1000):
    return fetch_data(
        endpoint="/posts/inspire",
        params={"page": page, "page_size": page_size},
        save_path=f"data/raw/inspired_posts_page_{page}.json"
    )

def get_all_rated_posts(page=1, page_size=1000):
    return fetch_data(
        endpoint="/posts/rating",
        params={"page": page, "page_size": page_size},
        save_path=f"data/raw/rated_posts_page_{page}.json"
    )
