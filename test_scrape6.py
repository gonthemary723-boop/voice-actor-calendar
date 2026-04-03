import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
import re
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# 確定リスト（手動確認済みID）
ACTOR_LIST = [
    {"name": "長月あおい", "id": 77017},
    {"name": "小鹿なお", "id": 56410},
    {"name": "飯田ヒカル", "id": 51873},
    {"name": "七瀬つむぎ", "id": 77781},
    {"name": "花岩香奈", "id": 77489},
    {"name": "伊藤舞音", "id": 77650},
    {"name": "湊みや", "id": 77243},
    {"name": "川村玲奈", "id": 77840},
    {"name": "薄井友里", "id": 56962},
    {"name": "松田彩音", "id": 77941},
    {"name": "春咲暖", "id": 16058},
    {"name": "陽高真白", "id": 67164},
    {"name": "天音ゆかり", "id": 81536},
    {"name": "浅見香月", "id": 78176},
]

TODAY = date.today()

def scrape_actor_events(actor_name, actor_id):
    """1人の声優の未来イベントを全ページ取得"""
    all_events = []
    page = 1
    
    while True:
        url = f"https://www.eventernote.com/actors/{actor_id}/events?page={page}"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        event_items = soup.select('ul.firing_list li.clearfix')
        if not event_items:
            break
        
        page_has_future = False
        
        for item in event_items:
            # 日付
            date_tag = item.select_one('div.firing_firing span.firing_firing_date a')
            if not date_tag:
                continue
            date_text = date_tag.get_text(strip=True)
            match = re.search(r'(\d{4})/(\d{1,2})/(\d{1,2})', date_text)
            if not match:
                continue
            event_date = date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
            
            # 過去イベントはスキップ
            if event_date < TODAY:
                continue
            
            page_has_future = True
            
            # イベント名
            title_tag = item.select_one('p.firing_firing_name span a')
            title = title_tag.get_text(strip=True) if title_tag else "不明"
            event_url = ""
            if title_tag and title_tag.get('href'):
                event_url = "https://www.eventernote.com" + title_tag['href']
            
            # 会場・時間
            place_div = item.select_one('div.firing_firing p.firing_place')
            venue = ""
            start_time = ""
            end_time = ""
            if place_div:
                place_text = place_div.get_text(strip=True)
                time_match = re.search(
                    r'開演(\d{1,2}:\d{2})(?:～終演(\d{1,2}:\d{2}))?', place_text
                )
                if time_match:
                    start_time = time_match.group(1)
                    end_time = time_match.group(2) or ""
                venue_text = re.sub(r'開演\d{1,2}:\d{2}(?:～終演\d{1,2}:\d{2})?', '', place_text).strip()
                venue = venue_text
            
            # 出演者
            actor_links = item.select('p.firing_firing_actor a')
            actors = [a.get_text(strip=True) for a in actor_links]
            
            all_events.append({
                'date': event_date.isoformat(),
                'title': title,
                'venue': venue,
                'start_time': start_time,
                'end_time': end_time,
                'actors': actors,
                'event_url': event_url,
                'source_actor': actor_name,
            })
        
        # 全て過去なら終了（ページは新しい順）
        if not page_has_future and event_items:
            break
        
        page += 1
        time.sleep(1)  # サーバー負荷軽減
    
    return all_events

def main():
    print("=== 全声優 未来イベント一括取得 ===")
    print(f"基準日: {TODAY}")
    print()
    
    total_events = []
    
    for actor in ACTOR_LIST:
        print(f"取得中: {actor['name']} (ID:{actor['id']}) ... ", end="", flush=True)
        events = scrape_actor_events(actor['name'], actor['id'])
        print(f"{len(events)}件")
        total_events.extend(events)
        time.sleep(2)  # 声優間のウェイト
    
    # 重複除去（同じ日付+同じタイトル）
    seen = set()
    unique_events = []
    for ev in total_events:
        key = (ev['date'], ev['title'])
        if key not in seen:
            seen.add(key)
            unique_events.append(ev)
    
    print()
    print("=" * 60)
    print(f"合計: {len(total_events)}件 → 重複除去後: {len(unique_events)}件")
    print("=" * 60)
    print()
    
    for ev in sorted(unique_events, key=lambda x: x['date']):
        time_str = f" {ev['start_time']}" if ev['start_time'] else ""
        actors_str = ", ".join(ev['actors'][:5])
        if len(ev['actors']) > 5:
            actors_str += f" 他{len(ev['actors'])-5}名"
        print(f"  {ev['date']}{time_str} | {ev['title'][:40]}")
        print(f"    会場: {ev['venue'][:30]}  出演: {actors_str}")
        print()

if __name__ == '__main__':
    main()
