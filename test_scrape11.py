import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

url = "https://www.eventernote.com/actors/16058/events?page=1"
response = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(response.text, 'html.parser')

# gb_event_list の中身全体の構造を確認
container = soup.find('div', class_='gb_event_list')
if container:
    print("=== gb_event_list 直下の子要素 ===")
    for child in container.children:
        if hasattr(child, 'name') and child.name:
            text_preview = child.get_text(strip=True)[:80]
            classes = child.get('class', [])
            print(f"  <{child.name}> class={classes} → {text_preview}")
else:
    print("gb_event_list が見つかりません")

print()

# 日付の別フォーマットを探す（年月日、YYYY-MM-DD など）
import re
# 日本語日付
jp_dates = re.findall(r'\d{4}年\d{1,2}月\d{1,2}日', response.text)
print(f"日本語日付: {len(jp_dates)}件 → {jp_dates[:5]}")

# ISO形式
iso_dates = re.findall(r'\d{4}-\d{2}-\d{2}', response.text)
print(f"ISO日付: {len(iso_dates)}件 → {iso_dates[:5]}")

# スラッシュ区切り（月/日のみ含む）
slash_dates = re.findall(r'\d{1,2}/\d{1,2}', response.text)
print(f"スラッシュ日付: {len(slash_dates)}件 → {slash_dates[:10]}")
