import re
import requests
from bs4 import BeautifulSoup

URL = "https://www.eventernote.com/actors/%E5%B0%8F%E9%B9%BF%E3%81%AA%E3%81%8A/56410/events"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def parse_events(soup):
    """イベント一覧をパースしてリストで返す"""
    events = []
    
    for li in soup.select('li.clearfix'):
        # 日付
        date_div = li.select_one('div.date')
        if not date_div:
            continue
        date_text = date_div.get_text(strip=True)
        # "2026-09-06 (日)" → "2026-09-06"
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', date_text)
        date = date_match.group(1) if date_match else '不明'
        
        # イベント名
        event_div = li.select_one('div.event')
        if not event_div:
            continue
        
        title_tag = event_div.select_one('h4 a')
        title = title_tag.get_text(strip=True) if title_tag else '不明'
        event_url = title_tag['href'] if title_tag else ''
        
        # 会場
        place_divs = event_div.select('div.place')
        venue = ''
        times = ''
        for p in place_divs:
            text = p.get_text(strip=True)
            if '会場' in text:
                venue_tag = p.select_one('a')
                venue = venue_tag.get_text(strip=True) if venue_tag else text.replace('会場:', '').strip()
            elif '開演' in text or '開場' in text:
                times = text
        
        # 開演時間を抽出
        start_match = re.search(r'開演\s*(\d{1,2}:\d{2})', times)
        end_match = re.search(r'終演\s*(\d{1,2}:\d{2})', times)
        start_time = start_match.group(1) if start_match else ''
        end_time = end_match.group(1) if end_match else ''
        
        # 出演者
        actors = []
        actor_div = event_div.select_one('div.actor')
        if actor_div:
            for a in actor_div.select('a'):
                actors.append(a.get_text(strip=True))
        
        events.append({
            'date': date,
            'title': title,
            'venue': venue,
            'start_time': start_time,
            'end_time': end_time,
            'actors': actors,
            'url': f"https://www.eventernote.com{event_url}",
        })
    
    return events

def main():
    print("=== Eventernote スクレイピング ===")
    print("対象：小鹿 なお")
    print()
    
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    events = parse_events(soup)
    
    print(f"取得イベント数: {len(events)}")
    print()
    
    for i, ev in enumerate(events, 1):
        print(f"--- {i}. {ev['date']} ---")
        print(f"  タイトル: {ev['title']}")
        print(f"  会場:     {ev['venue']}")
        print(f"  開演:     {ev['start_time']}")
        print(f"  終演:     {ev['end_time']}")
        print(f"  出演者:   {', '.join(ev['actors'])}")
        print(f"  URL:      {ev['url']}")
        print()

if __name__ == '__main__':
    main()
