import requests
from bs4 import BeautifulSoup

URL = "https://www.eventernote.com/actors/%E5%B0%8F%E9%B9%BF%E3%81%AA%E3%81%8A/56410/events"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def main():
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    # イベントリスト全体の親要素を探す
    # 日付見出しを探す
    print("=== 日付っぽい要素を探す ===")
    print()

    # h3, h2 タグを確認（日付見出しによく使われる）
    for tag in ['h1', 'h2', 'h3', 'h4', 'h5']:
        elements = soup.select(tag)
        for el in elements[:10]:
            text = el.get_text(strip=True)
            if any(c in text for c in ['月', '日', '2025', '2026', '/']):
                print(f"<{tag}>: {text}")

    print()
    print("=== date クラスを含む要素 ===")
    date_elements = soup.select('[class*="date"]')
    for el in date_elements[:10]:
        print(f"tag={el.name}, class={el.get('class')}, text={el.get_text(strip=True)}")

    print()
    print("=== イベント周辺のHTML（最初の1件分） ===")
    # イベントの親要素を確認
    first_event = soup.select_one('div.event')
    if first_event:
        parent = first_event.parent
        # 親の中の最初の部分だけ表示
        html = parent.prettify()
        print(html[:3000])

if __name__ == '__main__':
    main()
