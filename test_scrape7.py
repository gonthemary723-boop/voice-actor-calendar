import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# 春咲暖（ID:16058）- 最も活動歴が長いのでデータ多いはず
url = "https://www.eventernote.com/actors/16058/events?page=1"
response = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(response.text, 'html.parser')

items = soup.select('ul.firing_list li.clearfix')
print(f"取得件数: {len(items)}")

for item in items[:5]:
    date_tag = item.select_one('div.firing_firing span.firing_firing_date a')
    title_tag = item.select_one('p.firing_firing_name span a')
    d = date_tag.get_text(strip=True) if date_tag else "日付なし"
    t = title_tag.get_text(strip=True) if title_tag else "タイトルなし"
    print(f"  {d} | {t[:50]}")
