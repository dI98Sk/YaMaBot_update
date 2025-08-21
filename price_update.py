import gspread
import requests
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

class YandexMarketUpdater:
    def __init__(self, spreadsheet_url, credentials_file, oauth_token, business_id):
        self.SPREADSHEET_URL = spreadsheet_url
        self.CREDENTIALS_FILE = credentials_file
        self.OAUTH_TOKEN = oauth_token
        self.BUSINESS_ID = business_id

        # Авторизация в Google Sheets
        self.scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.CREDENTIALS_FILE, self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open_by_url(self.SPREADSHEET_URL).sheet1

        # Авторизация в Яндекс.Маркет API
        self.headers_auth = {
            "Authorization": f"Bearer {self.OAUTH_TOKEN}",
            "Content-Type": "application/json"
        }

    def get_offers_prices(self):
        rows = self.sheet.get_all_values()[1:]  # пропускаем заголовок
        offers_prices = []

        for row in rows:
            offer_id = row[1].strip()
            if not offer_id:
                continue

            price_str = row[3].replace(",", ".").strip()
            discount_str = row[4].replace(",", ".").strip()

            # Если нет цены или скидки — пропускаем товар
            if not price_str or not discount_str:
                print(f"[ℹ️] Товар без цены: {offer_id}. Пропускаем обновление.")
                continue

            try:
                price = float(price_str)
                discount_base = float(discount_str)

                if price <= 0 or discount_base <= 0:
                    print(f"[⚠️] Нулевая цена или скидка для товара {offer_id}. Пропущен.")
                    continue

            except ValueError as e:
                print(f"Пропущена строка с ошибочными данными: {row} (Ошибка: {e})")
                continue

            offers_prices.append({
                "offerId": offer_id,
                "price": {
                    "value": str(price),
                    "discountBase": str(discount_base),
                    "currencyId": "RUR"
                }
            })

        return offers_prices

    def update_prices(self, offers_prices):
        url_prices = f"https://api.partner.market.yandex.ru/v2/businesses/{self.BUSINESS_ID}/offer-prices/updates"
        resp_prices = requests.post(url_prices, json={"offers": offers_prices}, headers=self.headers_auth)

        if resp_prices.status_code == 200:
            print(f"[✅] Цены успешно обновлены. Отправлено {len(offers_prices)} позиций.")
        else:
            print(f"[❌] Ошибка при обновлении цен: {resp_prices.status_code}")
            try:
                print(resp_prices.json())  # 💡 Логируем JSON-ответ для диагностики
            except:
                print(resp_prices.text)

    def run(self):
        print(f"[🕒] Начало обновления: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Получение данных
        offers_prices = self.get_offers_prices()
        print(f"📦 Найдено товаров для обновления цен: {len(offers_prices)}")

        # Обновление цен
        self.update_prices(offers_prices)

        print(f"\n[🕒] Завершено: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


