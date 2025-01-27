import os
import json

import requests


class RequestHandler:
    def __init__(self):
        self.api_key: str = os.environ.get("API_KEY")
        self.url_trading: str = os.environ.get("TRADING_URL")
        self.url_market: str = os.environ.get("MARKET_URL")

    def get_data_trading(self, endpoint: str):
        response = requests.get(self.url_trading + endpoint, headers=self.headers)
        return response.json()

    def get_data_market(self, endpoint: str):
        response = requests.get(self.url_market + endpoint, headers=self.headers)
        return response.json()

    def put_data(self, endpoint: str):
        response = requests.put(self.url_trading + endpoint, headers=self.headers)
        return response.json()

    def post_data(self, endpoint: str, data):
        response = requests.post(
            self.url_trading + endpoint, json.dumps(data), headers=self.headers)
        return response.json()

    @property
    def headers(self):
        return {"Authorization": f"Bearer {self.api_key}"}


class LemonMarketsAPI(RequestHandler):
    def get_instrument(self, query: str):
        return self.get_data_market(f"instruments/?search={query}&type=stock&tradable=true")

    def place_order(
        self, isin: str, expires_at: str, quantity: int, side: str
    ):
        venue = os.environ.get("MIC")

        order_details = {
            "isin": isin,
            "expires_at": expires_at,
            "side": side,
            "quantity": quantity,
            "venue": venue
        }
        return self.post_data(f"orders/", order_details)

    def activate_order(self, order_id: str):
        return self.post_data(
            f"orders/{order_id}/activate/", {}
        )

    def get_portfolio(self) -> list:
        return self.get_data_trading(f"portfolio/")[
            "results"
        ]

    def get_venue(self):
        return self.get_data_market("venues/")["results"][0]
