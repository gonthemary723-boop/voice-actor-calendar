import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

url = "https://www.eventernote.com/actors/16058/events?page=1"
response = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(response.text, 'html.parser')

container = soup.find('div', class_='gb_event_list')
if not container:
    print("ERROR: gb_event_list が見つかりません")
    exit()

items = container.find_all('li', class_='clearfix')
print(f"取得イベント数: {len(items)}")
print()

for i, item in enumerate(items):
    # 日付
    date_p = item.find('div', class_='date')
    date_text = ""
    if date_p:
        p_tag = date_p.find('p')
        if p_tag:
            date_text = p_tag.get_text(strip=True)

    # 日付からISO部分だけ抽出
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', date_text)
    date_iso = date_match.group(1) if date_match else "不明"

    # イベント名・URL
    event_div = item.find('div', class_='event')
    event_name = ""
    event_url = ""
    if event_div:
        a_tag = event_div.find('h4')
        if a_tag:
            link = a_tag.find('a')
            if link:
                event_name = link.get_text(strip=True)
                event_url = link.get('href', '')

    # 会場
    place_divs = item.find_all('div', class_='place')
    venue = ""
    times = ""
    for pd in place_divs:
        a_tag = pd.find('a')
        if a_tag:
            venue = a_tag.get_text(strip=True)
        span_tag = pd.find('span', class_='s')
        if span_tag:
            times = span_tag.get_text(strip=True)

    # 出演者
    actor_div = item.find('div', class_='actor')
    actors = []
    if actor_div:
        for li in actor_div.find_all('li'):
            a_tag = li.find('a')
            if a_tag:
                actors.append(a_tag.get_text(strip=True))

    print(f"[{i+1}] {date_iso} | {event_name}")
    print(f"     会場: {venue}")
    print(f"     時間: {times}")
    print(f"     出演: {', '.join(actors[:5])}{'...' if len(actors) > 5 else ''}")
    print(f"     URL:  https://www.eventernote.com{event_url}")
    print()
