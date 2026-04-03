from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

# スコープ（カレンダーの読み書き権限）
SCOPES = ['https://www.googleapis.com/auth/calendar']

# credentials.json のパス
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), 'credentials.json')

def main():
    print("=== Google Calendar 認証テスト ===")
    print()

    # OAuth認証フロー開始
    print("ブラウザが開きます。Googleアカウントでログインしてください。")
    print()

    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
    creds = flow.run_local_server(port=0)

    # カレンダーAPIに接続
    service = build('calendar', 'v3', credentials=creds)

    # カレンダー一覧を取得
    calendar_list = service.calendarList().list().execute()

    print("✅ 認証成功！")
    print()
    print("あなたのカレンダー一覧：")
    for calendar in calendar_list['items']:
        print(f"  - {calendar['summary']}")

    print()
    print("=== テスト完了 ===")

if __name__ == '__main__':
    main()