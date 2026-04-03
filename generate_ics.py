# generate_ics.py
"""
Eventernote JSON → ICS (iCalendar) 変換スクリプト
"""

import hashlib
import json
from datetime import datetime, timezone


# === データ読み込み ===

def load_events(json_path: str) -> tuple[dict, list[dict]]:
    """JSONファイルからイベントデータを読み込む"""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    actor = {
        "id": data["actor_id"],
        "name": data["actor_name"],
    }
    return actor, data["events"]


# === UID 生成 ===

def generate_uid(event: dict) -> str:
    """イベントからユニークIDを生成する"""
    raw = f"{event['event_url']}_{event['date']}"
    return hashlib.md5(raw.encode()).hexdigest() + "@voice-actor-calendar"


# === 日時パース ===

def parse_date(date_str: str) -> str:
    """日付文字列をICS形式に変換 (YYYYMMDD)"""
    date_str = date_str.strip()
    for ch in ["年", "月"]:
        date_str = date_str.replace(ch, "-")
    date_str = date_str.split("日")[0]
    parts = date_str.split("-")
    return f"{int(parts[0]):04d}{int(parts[1]):02d}{int(parts[2]):02d}"


def parse_time(time_str: str) -> str:
    """時刻文字列をICS形式に変換 (HHMMSS)"""
    time_str = time_str.strip().replace("：", ":")
    parts = time_str.split(":")
    return f"{int(parts[0]):02d}{int(parts[1]):02d}00"


def get_dtstart(event: dict) -> str:
    """開始日時のICS表現を返す"""
    date_ics = parse_date(event["date"])
    start = event.get("start_time", "").strip()
    if start:
        time_ics = parse_time(start)
        return f"DTSTART;TZID=Asia/Tokyo:{date_ics}T{time_ics}"
    else:
        return f"DTSTART;VALUE=DATE:{date_ics}"


def get_dtend(event: dict) -> str:
    """終了日時のICS表現を返す（開演+2時間 or 終日）"""
    date_ics = parse_date(event["date"])
    start = event.get("start_time", "").strip()
    if start:
        time_ics = parse_time(start)
        h = int(time_ics[:2]) + 2
        if h >= 24:
            h -= 24
        end_time = f"{h:02d}{time_ics[2:]}"
        return f"DTEND;TZID=Asia/Tokyo:{date_ics}T{end_time}"
    else:
        from datetime import timedelta
        dt = datetime.strptime(date_ics, "%Y%m%d")
        next_day = (dt + timedelta(days=1)).strftime("%Y%m%d")
        return f"DTEND;VALUE=DATE:{next_day}"


# === 説明文 ===

def build_description(event: dict, actor_name: str) -> str:
    """イベントの説明文を組み立てる"""
    lines = []

    # 会場（最優先）
    if event.get("venue"):
        lines.append(f"会場: {event['venue']}")

    # 開場/開演を1行にまとめる
    times = []
    if event.get("open_time"):
        times.append(f"開場 {event['open_time']}")
    if event.get("start_time"):
        times.append(f"開演 {event['start_time']}")
    if times:
        lines.append(" / ".join(times))

    # 出演者（自分以外を最大20名表示）
    actors = event.get("actors", [])
    others = [a["name"] for a in actors if a.get("name") != actor_name]
    if others:
        display = others[:20]
        lines.append(f"共演: {', '.join(display)}")
        if len(others) > 20:
            lines.append(f"  ...他{len(others) - 20}名")

    # Eventernoteリンク
    url = event["event_url"]
    if not url.startswith("http"):
        url = f"https://www.eventernote.com{url}"
    lines.append(url)

    return "\n".join(lines)


# === ICSテキスト生成 ===

def escape_ics_text(text: str) -> str:
    """ICSのテキストフィールド用エスケープ"""
    text = text.replace("\\", "\\\\")
    text = text.replace(";", "\\;")
    text = text.replace(",", "\\,")
    return text


def fold_line(line: str) -> str:
    """ICS仕様に従い、75オクテットで行を折り返す（RFC 5545 Section 3.1）"""
    encoded = line.encode("utf-8")
    if len(encoded) <= 75:
        return line
    
    result = []
    current = b""
    for char in line:
        char_bytes = char.encode("utf-8")
        # 最初の行は75、継続行は74（先頭スペース分）
        limit = 75 if not result else 74
        if len(current) + len(char_bytes) > limit:
            result.append(current.decode("utf-8"))
            current = char_bytes
        else:
            current += char_bytes
    if current:
        result.append(current.decode("utf-8"))
    
    return "\r\n ".join(result)


def event_to_vevent(event: dict, actor_name: str) -> list[str]:
    """1イベントをVEVENTの行リストに変換する"""
    now_utc = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    description = build_description(event, actor_name)
    summary = escape_ics_text(event["event_name"])
    location = escape_ics_text(event.get("venue", "") or "")

    lines = [
        "BEGIN:VEVENT",
        f"UID:{generate_uid(event)}",
        f"DTSTAMP:{now_utc}",
        get_dtstart(event),
        get_dtend(event),
        f"SUMMARY:{summary}",
    ]
    if location:
        lines.append(f"LOCATION:{location}")

    # DESCRIPTIONは各行を escape してから \n で結合
    desc_lines = description.split("\n")
    escaped_desc = "\\n".join(escape_ics_text(line) for line in desc_lines)
    lines.append(f"DESCRIPTION:{escaped_desc}")

    lines.append("END:VEVENT")
    return lines


# === メイン処理 ===

def generate_ics(json_path: str):
    """JSONからICSファイルを生成する"""
    actor, events = load_events(json_path)
    actor_name = actor["name"]
    actor_id = actor["id"]

    cal_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//voice-actor-calendar//EN",
        f"X-WR-CALNAME:{actor_name}のイベント",
        "CALSCALE:GREGORIAN",
        "BEGIN:VTIMEZONE",
        "TZID:Asia/Tokyo",
        "BEGIN:STANDARD",
        "DTSTART:19700101T000000",
        "TZOFFSETFROM:+0900",
        "TZOFFSETTO:+0900",
        "TZNAME:JST",
        "END:STANDARD",
        "END:VTIMEZONE",
    ]

    for event in events:
        vevent_lines = event_to_vevent(event, actor_name)
        cal_lines.extend(vevent_lines)

    cal_lines.append("END:VCALENDAR")

    output_path = f"data/calendar_{actor_id}.ics"
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        for line in cal_lines:
            stripped = line.strip()
            if stripped:
                f.write(fold_line(stripped) + "\r\n")


    print(f"ICSファイル生成完了: {output_path}")
    print(f"  イベント数: {len(events)}件")
    print(f"  カレンダー名: {actor_name}のイベント")


if __name__ == "__main__":
    generate_ics("data/actor_16058.json")
