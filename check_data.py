"""取得データの確認スクリプト"""

import json
from pathlib import Path

filepath = Path("data/actor_16058.json")
data = json.loads(filepath.read_text(encoding="utf-8"))

print(f"声優: {data['actor_name']}（ID: {data['actor_id']}）")
print(f"取得日時: {data['fetched_at']}")
print(f"イベント数: {data['event_count']}")

events = data["events"]

# 日付の範囲
dates = [e["date"] for e in events if e["date"]]
print(f"期間: {min(dates)} ～ {max(dates)}")

# 会場が空のイベント数
no_venue = sum(1 for e in events if not e["venue"])
print(f"会場なし: {no_venue}件")

# 開演時間が空のイベント数
no_start = sum(1 for e in events if not e["start_time"])
print(f"開演時間なし: {no_start}件")

# 出演者数の統計
actor_counts = [len(e["actors"]) for e in events]
print(f"出演者数: 最小{min(actor_counts)} / 最大{max(actor_counts)} / 平均{sum(actor_counts)/len(actor_counts):.1f}")

# 最古のイベント5件
print(f"\n--- 最古の5件 ---")
oldest = sorted(events, key=lambda e: e["date"] or "9999")[:5]
for e in oldest:
    print(f"  {e['date']} | {e['event_name'][:60]}")
