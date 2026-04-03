import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

url = "https://www.eventernote.com/actors/16058/events?page=1"
response = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(response.text, 'html.parser')

# div.event の中身を3件だけ詳しく表示
events = soup.find_all('div', class_='event')
print(f"div.event 件数: {len(events)}")
print()

for i, ev in enumerate(events[:3]):
    print(f"=== イベント {i+1} ===")
    print(ev.prettify()[:1500])
    print("---")
    print()
