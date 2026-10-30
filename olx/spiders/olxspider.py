from urllib.parse import urlencode

import scrapy


class OlxspiderSpider(scrapy.Spider):
    name = "olxspider"
    allowed_domains = ["olx.co.id"]
    page = 0

    # # alternative setting on setting.py
    # custom_settings = {
    #     "DOWNLOAD_DELAY": 1,
    #     "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
    #     "COOKIES_ENABLED": True,  # fetch used credentials: "include"
    # }

    API_URL = "https://www.olx.co.id/api/relevance/v6/search"

    PARAMS = {
        "category": "5160",
        "facet_limit": "100",
        "location": "5000496",
        "location_facet_limit": "20",
        "platform": "web-desktop",
        "relaxedFilters": "true",
        "user": "1a180aa6eb5x6ffb900d",
    }

    # # alternative setting on setting.py
    # HEADERS = {
    #     "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:159.0) Gecko/20100101 Firefox/159.0",
    #     "Accept": "*/*",
    #     "Accept-Language": "en-US,en;q=0.9",
    #     "X-Panamera-fingerprint": "a57bc718f955b6daecc612cf2f8a6a51#1793160018617",
    #     "Alt-Used": "www.olx.co.id",
    #     "Sec-Fetch-Dest": "empty",
    #     "Sec-Fetch-Mode": "cors",
    #     "Sec-Fetch-Site": "same-origin",
    #     "Priority": "u=4",
    #     # fetch's "referrer" option -> Referer header
    #     "Referer": "https://www.olx.co.id/jatinegara_g5000496/disewakan-rumah-apartemen_c5160",
    # }

    def _api_request(self, url):
        return scrapy.Request(
            url,
            method="GET",
            # headers=self.HEADERS, # already set on setting.py
            callback=self.parse,
            errback=self.on_error,
        )

    def _initial_requests(self):
        yield self._api_request(f"{self.API_URL}?{urlencode(self.PARAMS)}")

    async def start(self):
        for request in self._initial_requests():
            yield request

    def parse(self, response):
        payload = response.json()

        for ad in payload.get("data", []):
            price = (ad.get("price") or {}).get("value") or {}
            yield {
                "id": ad.get("id"),
                "title": ad.get("title"),
                "description": ad.get("description"),
                "price_raw": price.get("raw"),
                "price_display": price.get("display"),
                "location": ad.get("locations_resolved"),
                "created_at": ad.get("created_at"),
                "parameters": ad.get("parameters"),
            }

        # Pagination: follow the API's next-page link if it provides one
        next_url = (payload.get("metadata") or {}).get("next_page_url")
        if next_url:
            self.page += 1
            yield self._api_request(f"{self.API_URL}?{urlencode(self.PARAMS | {"page": self.page})}")

    def on_error(self, failure):
        self.logger.error("Request failed: %r", failure)
