"""
Run this once (from backend/ folder, with venv active) to see what
requests.get() is actually pulling back from Flipkart/Amazon.

    python debug_fetch.py

Paste the printed output back to Claude for diagnosis.
"""
import requests
from bs4 import BeautifulSoup

url = "https://www.flipkart.com/oppo-a78-5g-glowing-black-128-gb/p/itmf1eeaf323aaa5"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept-Language": "en-IN,en;q=0.9",
}

response = requests.get(url, headers=headers, timeout=10)
print("STATUS CODE:", response.status_code)
print("RESPONSE LENGTH (chars):", len(response.text))
print("\n--- FIRST 1500 CHARS OF RAW HTML ---\n")
print(response.text[:1500])

soup = BeautifulSoup(response.text, "html.parser")
print("\n--- PAGE TITLE TAG ---")
print(soup.title.string if soup.title else "No <title> found")

print("\n--- VISIBLE TEXT (first 800 chars) ---")
for tag in soup(["script", "style"]):
    tag.decompose()
print(soup.get_text(separator=" ", strip=True)[:800])