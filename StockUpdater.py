import gspread
import requests
import json
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials


class StockUpdaterFBS:
    def __init__(self, spreadsheet_url, credentials_file, oauth_token, warehouse_id, campaign_id):
        self.SPREADSHEET_URL = spreadsheet_url
        self.CREDENTIALS_FILE = credentials_file
        self.OAUTH_TOKEN = oauth_token
        self.WAREHOUSE_ID = warehouse_id
        self.headers_auth = {
            "Authorization": f"Bearer {self.OAUTH_TOKEN}",
            "Content-Type": "application/json"
        }

        self.CAMPAIGN_ID = campaign_id
        # self.CAMPAIGN_ID = self.get_campaign_id()

        self.scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.CREDENTIALS_FILE, self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open_by_url(self.SPREADSHEET_URL).sheet1

    def get_warehouses(self):
        url = f"https://api.partner.market.yandex.ru/v2/campaigns/{self.CAMPAIGN_ID}/warehouses"
        response = requests.get(url, headers=self.headers_auth)
        if response.status_code == 200:
            warehouses = response.json().get("warehouses", [])
            ids = [w["id"] for w in warehouses]
            print(f"[ℹ️] Доступные склады кампании {self.CAMPAIGN_ID}: {ids}")
            return ids
        else:
            print(f"[❌] Ошибка получения складов: {response.status_code}")
            print(response.text)
            return []

    def get_campaign_id(self):
        url = "https://api.partner.market.yandex.ru/v2/campaigns"
        response = requests.get(url, headers=self.headers_auth)
        if response.status_code == 200:
            data = response.json()
            print("Полученные кампании:", data)  # ⬅️
            for campaign in data.get("campaigns", []):
                if campaign.get("placementType") == "FBS":
                    print(f"✅ Найдена кампания FBS: {campaign['id']}")
                    return campaign["id"]
        else:
            print(f"[❌] Ошибка получения campaignId: {response.status_code}")
            print(response.text)
        return None

    def find_campaign_with_warehouse(self, target_warehouse_id):
        url = "https://api.partner.market.yandex.ru/v2/campaigns"
        response = requests.get(url, headers=self.headers_auth)
        if response.status_code != 200:
            print("[❌] Не удалось получить список кампаний")
            print(response.text)
            return

        data = response.json()
        for campaign in data.get("campaigns", []):
            campaign_id = campaign["id"]
            placement = campaign.get("placementType")
            if placement != "FBS":
                continue

            url = f"https://api.partner.market.yandex.ru/v2/campaigns/{campaign_id}/warehouses"
            wh_response = requests.get(url, headers=self.headers_auth)
            if wh_response.status_code == 200:
                warehouses = wh_response.json().get("warehouses", [])
                for wh in warehouses:
                    if str(wh["id"]) == str(target_warehouse_id):
                        print(f"✅ Найдена подходящая кампания: {campaign_id} с нужным складом {target_warehouse_id}")
                        return campaign_id
            else:
                print(f"[⚠️] Кампания {campaign_id}: ошибка получения складов ({wh_response.status_code})")

        print("[❌] Не найдена кампания с указанным складом.")
        return None

    def get_offers_stocks(self):
        rows = self.sheet.get_all_values()[1:]  # пропустить заголовки
        offers_stocks = []

        for row in rows:
            offer_id = row[1].strip()
            if not offer_id:
                continue

            offers_stocks.append({
                "sku": offer_id,
                "warehouseId": self.WAREHOUSE_ID,
                "items": [{"count": 2, "type": "FIT"}]  # по умолчанию 2
            })

        return offers_stocks

    def update_stocks(self, offers_stocks):
        url = f"https://api.partner.market.yandex.ru/v2/campaigns/{self.CAMPAIGN_ID}/warehouses/{self.WAREHOUSE_ID}/stocks"
        print("[📦] Payload:")
        print(json.dumps({"skus": offers_stocks}, indent=2, ensure_ascii=False))
        resp = requests.put(url, json={"skus": offers_stocks}, headers=self.headers_auth)

        if resp.status_code == 200:
            print(f"[✅] Остатки успешно обновлены. Отправлено {len(offers_stocks)} позиций.")
        else:
            print(f"[❌] Ошибка при обновлении остатков: {resp.status_code}")
            try:
                print(resp.json())
            except:
                print(resp.text)

    def run(self):
        print(f"[🕒] Начало обновления остатков: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        if not self.CAMPAIGN_ID:
            print("[❌] Campaign ID не получен. Прерываем обновление.")
            return

        offers_stocks = self.get_offers_stocks()
        # self.get_warehouses()

        valid_warehouses = self.get_warehouses()
        if self.WAREHOUSE_ID not in [str(w) for w in valid_warehouses]:
            print(f"[❌] Склад {self.WAREHOUSE_ID} не найден у кампании {self.CAMPAIGN_ID}. Прерываем.")
            return

        self.update_stocks(offers_stocks)
        print(f"[🕒] Завершено обновление остатков: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


# Пример запуска
if __name__ == "__main__":
    updater = StockUpdaterFBS(
        spreadsheet_url="https://docs.google.com/spreadsheets/d/1-0fSX404BKuzZRCgVflyNT-4icIDOnmF4cyaHdkrz6Y/edit",
        credentials_file="credentials.json",
        oauth_token="y0__xDEs9qFCBi8wTcg2-3egBMXHkXGe2pQwTFnO0gJ5AnWgTeC7Q",
        warehouse_id="1749666",
        campaign_id='143409656'
    )
    # updater.run()
    campaign_id = updater.find_campaign_with_warehouse("1749666")
    if campaign_id:
        updater.CAMPAIGN_ID = campaign_id
        updater.run()

    # У тебя есть несколько FBS-кампаний:
    # - 143409656 → MobileBox ✅
    # - 147323103 → Android stock ✅
    # - 148619429 → Apple Stock ✅