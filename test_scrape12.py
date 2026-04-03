import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

url = "https://www.eventernote.com/actors/16058/events?page=1"
response = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(response.text, 'html.parser')

container = soup.find('div', class_='gb_event_list')
ul = container.find('ul') if container else None

if ul:
    print("=== ul 直下の子要素（最初の30個） ===")
    count = 0
    for child in ul.children:
        if hasattr(child, 'name') and child.name:
            classes = child.get('class', [])
            text = child.get_text(strip=True)[:100]
            # 最初の部分のHTMLも表示
            html_preview = str(child)[:200]
            print(f"\n[{count}] <{child.name}> class={classes}")
            print(f"  text: {text}")
            print(f"  html: {html_preview}")
            count += 1
            if count >= 8:
                break
else:
    print("ul が見つかりません")
