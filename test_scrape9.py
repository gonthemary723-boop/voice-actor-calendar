import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

url = "https://www.eventernote.com/actors/16058/events?page=1"
response = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(response.text, 'html.parser')

# どんなクラスのulやliがあるか調査
print("=== ul タグ一覧（class付き） ===")
for ul in soup.find_all('ul', class_=True):
    classes = ul.get('class', [])
    children = len(ul.find_all('li', recursive=False))
    print(f"  ul.{'.'.join(classes)} → li数: {children}")

print()
print("=== 'event' を含むクラス検索 ===")
for tag in soup.find_all(True, class_=True):
    for cls in tag.get('class', []):
        if 'event' in cls.lower() or 'firing' in cls.lower() or 'live' in cls.lower():
            print(f"  <{tag.name}> class='{cls}' → 子要素数:{len(tag.find_all(recursive=False))}")
            break

print()
print("=== 日付っぽいテキスト検索 ===")
import re
dates_found = re.findall(r'\d{4}/\d{1,2}/\d{1,2}', response.text)
print(f"  日付パターン数: {len(dates_found)}")
if dates_found:
    print(f"  先頭5件: {dates_found[:5]}")
    print(f"  末尾5件: {dates_found[-5:]}")
