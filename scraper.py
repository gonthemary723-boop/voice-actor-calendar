"""
eventernote スクレイパー
声優のイベント情報を取得して JSON で保存する
"""

import json
import re
import time
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
BASE_URL = "https://www.eventernote.com"
REQUEST_INTERVAL = 2  # 秒（サーバー負荷軽減）
DATA_DIR = Path("data")


def fetch_actor_events(actor_id: int, max_pages: int = 10) -> list[dict]:
    """指定声優の全イベントを取得する"""
    all_events = []

    for page in range(1, max_pages + 1):
        url = f"{BASE_URL}/actors/{actor_id}/events?page={page}"
        print(f"  ページ {page} 取得中: {url}")

        try:
            response = requests.get(url, headers=HEADERS, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"  ERROR: {e}")
            break

        events = parse_event_page(response.text)

        if not events:
            print(f"  ページ {page}: イベントなし → 終了")
            break

        all_events.extend(events)
        print(f"  ページ {page}: {len(events)}件取得（累計 {len(all_events)}件）")

        time.sleep(REQUEST_INTERVAL)

    return all_events


def parse_event_page(html: str) -> list[dict]:
    """1ページ分のHTMLからイベント情報をパースする"""
    soup = BeautifulSoup(html, "html.parser")
    events = []

    container = soup.find("div", class_="gb_event_list")
    if not container:
        return events

    items = container.find_all("li", class_="clearfix")

    for item in items:
        event = parse_event_item(item)
        if event:
            events.append(event)

    return events


def parse_event_item(item) -> dict | None:
    """li.clearfix 1つからイベント情報を抽出する"""

    # --- 日付 ---
    date_iso = ""
    date_div = item.find("div", class_="date")
    if date_div:
        p_tag = date_div.find("p")
        if p_tag:
            date_text = p_tag.get_text(strip=True)
            match = re.search(r"(\d{4}-\d{2}-\d{2})", date_text)
            if match:
                date_iso = match.group(1)

    # --- イベント名・URL ---
    event_name = ""
    event_url = ""
    event_div = item.find("div", class_="event")
    if event_div:
        h4 = event_div.find("h4")
        if h4:
            a_tag = h4.find("a")
            if a_tag:
                event_name = a_tag.get_text(strip=True)
                event_url = a_tag.get("href", "")

    if not event_name:
        return None

    # --- 会場・時間 ---
    venue = ""
    open_time = ""
    start_time = ""

    place_divs = item.find_all("div", class_="place")
    for pd in place_divs:
        a_tag = pd.find("a")
        if a_tag and not venue:
            venue = a_tag.get_text(strip=True)

        span_tag = pd.find("span", class_="s")
        if span_tag:
            time_text = span_tag.get_text(strip=True)
            open_match = re.search(r"開場\s*(\d{1,2}:\d{2})", time_text)
            start_match = re.search(r"開演\s*(\d{1,2}:\d{2})", time_text)
            if open_match:
                open_time = open_match.group(1)
            if start_match:
                start_time = start_match.group(1)

    # --- 出演者 ---
    actors = []
    actor_div = item.find("div", class_="actor")
    if actor_div:
        for li in actor_div.find_all("li"):
            a_tag = li.find("a")
            if a_tag:
                actor_name = a_tag.get_text(strip=True)
                actor_href = a_tag.get("href", "")
                actor_id_match = re.search(r"/actors/(\d+)", actor_href)
                actors.append(
                    {
                        "name": actor_name,
                        "id": int(actor_id_match.group(1))
                        if actor_id_match
                        else None,
                    }
                )

    return {
        "event_name": event_name,
        "event_url": f"{BASE_URL}{event_url}" if event_url else "",
        "date": date_iso,
        "venue": venue,
        "open_time": open_time,
        "start_time": start_time,
        "actors": actors,
    }


def save_events(actor_id: int, actor_name: str, events: list[dict]) -> Path:
    """イベント情報をJSONファイルに保存する"""
    DATA_DIR.mkdir(exist_ok=True)

    output = {
        "actor_id": actor_id,
        "actor_name": actor_name,
        "fetched_at": datetime.now().isoformat(),
        "event_count": len(events),
        "events": events,
    }

    filepath = DATA_DIR / f"actor_{actor_id}.json"
    filepath.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    return filepath


def main():
    """テスト実行：春咲暖（ID: 16058）"""
    actor_id = 16058
    actor_name = "春咲暖"

    print(f"=== {actor_name}（ID: {actor_id}）のイベント取得開始 ===")
    events = fetch_actor_events(actor_id, max_pages=50)
    print(f"\n合計 {len(events)} 件取得")

    if events:
        filepath = save_events(actor_id, actor_name, events)
        print(f"保存先: {filepath}")

        print(f"\n--- 直近5件 ---")
        for e in events[:5]:
            print(f"  {e['date']} | {e['event_name'][:50]}")
            print(f"    会場: {e['venue']}")
            print(f"    開演: {e['start_time'] or '未定'}")


if __name__ == "__main__":
    main()
