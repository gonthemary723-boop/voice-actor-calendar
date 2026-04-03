import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

url = "https://www.eventernote.com/actors/16058/events?page=1"
response = requests.get(url, headers=HEADERS)

print(f"Status: {response.status_code}")
print(f"URL: {response.url}")
print(f"Content-Length: {len(response.text)}")
print()
print("=== 先頭2000文字 ===")
print(response.text[:2000])
print()
print("=== 末尾1000文字 ===")
print(response.text[-1000:])
