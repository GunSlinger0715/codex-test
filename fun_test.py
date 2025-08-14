import requests
import random

BASE = "https://jsonplaceholder.typicode.com"

def random_post():
    post_id = random.randint(1, 100)
    r = requests.get(f"{BASE}/posts/{post_id}", timeout=10)
    r.raise_for_status()
    data = r.json()
    print(f"Random Post #{post_id}: {data['title']}")

if __name__ == "__main__":
    random_post()
