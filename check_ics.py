# check_ics.py
with open("data/calendar_16058.ics", "r", encoding="utf-8") as f:
    content = f.read()

empty_lines = content.count("\n\n")
print(f"空行の数: {empty_lines}")

events = content.split("BEGIN:VEVENT")
print(f"VEVENTブロック数: {len(events) - 1}")

if len(events) > 1:
    first = events[1].split("END:VEVENT")[0]
    print("--- 最初のイベント ---")
    print("BEGIN:VEVENT" + first + "END:VEVENT")
