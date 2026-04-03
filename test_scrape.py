import requests
from bs4 import BeautifulSoup

# 小鹿なおさんのイベントページ
URL = "https://www.eventernote.com/actors/%E5%B0%8F%E9%B9%BF%E3%81%AA%E3%81%8A/56410/events"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def main():
    print("=== Eventernote スクレイピングテスト ===")
    print("対象：小鹿 なお")
    print()

    response = requests.get(URL, headers=HEADERS)
    print(f"HTTPステータス: {response.status_code}")
    print()

    if response.status_code != 200:
        print("ページの取得に失敗しました")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # イベント一覧を探す
    events = soup.select('div.event')
    
    if not events:
        # 別のセレクタを試す
        events = soup.select('li.event')
    
    if not events:
        # ページ構造を確認するためHTMLを一部出力
        print("イベント要素が見つかりません。ページ構造を確認します...")
        print()
        print("--- HTML先頭2000文字 ---")
        print(response.text[:2000])
        print()
        print("--- タイトルタグ ---")
        title = soup.find('title')
        print(f"タイトル: {title.text if title else '不明'}")
        return

    print(f"イベント数: {len(events)}")
    print()

    for i, event in enumerate(events[:5], 1):
        print(f"--- イベント {i} ---")
        print(event.get_text(strip=True, separator=' | '))
        print()

if __name__ == '__main__':
    main()
