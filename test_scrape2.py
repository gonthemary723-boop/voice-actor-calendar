import requests
from bs4 import BeautifulSoup

URL = "https://www.eventernote.com/actors/%E5%B0%8F%E9%B9%BF%E3%81%AA%E3%81%8A/56410/events"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def main():
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    events = soup.select('div.event, li.event')

    print(f"イベント数: {len(events)}")
    print()

    # 最初の3件のHTML構造を詳しく表示
    for i, event in enumerate(events[:3], 1):
        print(f"=== イベント {i} のHTML構造 ===")
        print(event.prettify())
        print()
        print("=" * 60)
        print()

if __name__ == '__main__':
    main()
