import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# 学園アイドルマスター 声優14名
ACTORS = [
    "長月あおい",
    "小鹿なお",
    "飯田ヒカル",
    "七瀬つむぎ",
    "花岩香奈",
    "伊藤舞音",
    "湊みや",
    "川村玲奈",
    "薄井友里",
    "松田彩音",
    "春咲暖",
    "陽高真白",
    "天音ゆかり",
    "浅見香月",
]

def search_actor(name):
    """Eventernoteで声優名を検索してID・URLを取得"""
    search_url = f"https://www.eventernote.com/actors/search?keyword={quote(name)}"
    response = requests.get(search_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for a in soup.select('a[href*="/actors/"]'):
        href = a.get('href', '')
        parts = href.strip('/').split('/')
        if len(parts) >= 3 and parts[0] == 'actors':
            try:
                actor_id = int(parts[2])
                actor_name = a.get_text(strip=True)
                return {
                    'name': name,
                    'found_name': actor_name,
                    'id': actor_id,
                    'url': f"https://www.eventernote.com{href}",
                }
            except (ValueError, IndexError):
                continue
    
    return None

def main():
    print("=== Eventernote 声優ID検索 ===")
    print()
    
    results = []
    for name in ACTORS:
        print(f"検索中: {name} ... ", end="", flush=True)
        result = search_actor(name)
        if result:
            print(f"✅ ID={result['id']} ({result['found_name']})")
            results.append(result)
        else:
            print("❌ 見つかりません")
            results.append({'name': name, 'found_name': '', 'id': None, 'url': ''})
    
    print()
    print("=" * 60)
    print("結果一覧（コード用）:")
    print("=" * 60)
    print()
    print("ACTOR_LIST = [")
    for r in results:
        if r['id']:
            print(f'    {{"name": "{r["name"]}", "id": {r["id"]}}},')
        else:
            print(f'    # {{"name": "{r["name"]}", "id": ???}},  # 要手動確認')
    print("]")

if __name__ == '__main__':
    main()
