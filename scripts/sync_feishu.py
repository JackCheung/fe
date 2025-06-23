import os
import json
import requests
from datetime import datetime

# 飞书API配置
APP_ID = os.getenv('cli_a8d26e1915f3900b')
APP_SECRET = os.getenv('PYa3e3er0VxMZ9XQUFQ3gk4i01ZQE7IW')
APP_TOKEN = os.getenv('FdOmwRmwXioMqZkr341c6OhZnKf')  # 多维表格token
TABLE_ID = os.getenv('tbleEcX33ILMY9Mt')   # 表格ID

def get_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json"}
    payload = {"app_id": APP_ID, "app_secret": APP_SECRET}
    response = requests.post(url, headers=headers, json=payload)
    return response.json().get('tenant_access_token')

def fetch_feishu_data():
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records"
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json().get('data', {}).get('items', [])

def save_to_json(data):
    with open('docs/data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    records = fetch_feishu_data()
    formatted_data = [{"id": r["record_id"], **r["fields"]} for r in records]
    save_to_json(formatted_data)
    print(f"✅ Synced {len(records)} records at {datetime.now()}")
