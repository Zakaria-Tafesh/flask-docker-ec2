import json
# import time
import traceback

import requests
# from requests_html import HTMLSession
from dataclasses import dataclass
from input.config import headers_fresh, api_fresh_list, api_fresh_map, headers_toronto, api_toronto_list, api_toronto_map
from utils.logger import logger


@dataclass
class Home:
    Address: str
    Postal_Code: str
    Province: str
    City: str
    Neighbourhood: str
    Homeowner: str
    Price: str


@dataclass
class Response:
    response_text: str
    response_json: dict = None

    def run(self):
        try:
            self.convert_to_json()
            homes = self.get_homes()
            print(len(homes))
            print(homes)
            return homes
        except:
            traceback.print_exc()

    def convert_to_json(self):
        logger.info('convert_to_json')
        logger.info(self.response_text)
        logger.info(self.response_json)
        resp_json = json.loads(self.response_text)
        # print(type(resp_json))
        # print(resp_json)
        self.response_json = resp_json
        return resp_json

    def get_homes(self) -> list:
        if not self.response_json:
            return []
        return self.response_json['properties']


@dataclass
class Request:
    url: str = None
    payload: dict = None
    source: str = None
    page_num: int = 1
    render_page: bool = False
    status_code: int = 400
    response_json: dict = None
    session: None = None
    headers: dict = None
    api_list: str = None
    api_map: str = None

    def update_params(self):
        print('Updating Params')
        if self.source == 'freshrealty':
            self.headers = headers_fresh
            self.api_list = api_fresh_list
            self.api_map = api_fresh_map
        elif self.source == 'torontoPH':
            self.headers = headers_toronto
            self.api_list = api_toronto_list
            self.api_map = api_toronto_map

    def request(self):
        def update_header():
            logger.info('update_header')
            self.session.headers.update({
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            })

        def request_normal():
            logger.info('request_normal')
            self.session = requests.Session()
            update_header()
            res_n = self.session.get(url=self.url)
            return res_n

        # def request_html():
        #     logger.info('request_html')
        #     self.session = HTMLSession()
        #     update_header()
        #     res_h = self.session.get(self.url)
        #     res_h.html.render(sleep=5, keep_page=True, scrolldown=2)
        #     a = res_h.html.find('#lw${mlsId}')
        #     print(a)
        #     return res_h
        self.update_params()

        if self.render_page:
            res = request_normal()
        else:
            res = request_normal()
        logger.info(res.text)
        return res.status_code

    def call_map(self):
        logger.info('call_map')
        self.update_params()
        self.headers = {'authority': 'www.torontopropertyhunters.com', 'method': 'POST', 'path': '/property-search/res/includes/search_application/get_listings_for_map.asp', 'scheme': 'https', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.9,ar-AE;q=0.8,ar;q=0.7', 'Cache-Control': 'no-cache', 'Content-Type': 'application/x-www-form-urlencoded', 'Origin': 'https://www.torontopropertyhunters.com', 'Referer': 'https://www.torontopropertyhunters.com/property-search/results/', 'User-Agent ': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36', 'X-Kl-Ajax-Request': 'Ajax_Request', 'X-Requested-With': 'XMLHttpRequest'}

        logger.info(f'self.api_map {self.api_map}')
        logger.info(f'self.headers {self.headers}')
        logger.info(f'self.payload {self.payload}')

        response = requests.post(self.api_map, data=self.payload, headers=self.headers, params={"": ""})
        logger.info(response.status_code)

        if response.status_code == 200:
            resp_text = response.text
            logger.info(resp_text[:100])
            return resp_text


# if __name__ == "__main__":
#     for client in clients_list:
#         payload = client['payload_fresh_map']
#         name = client['client_name']
#         r = Request(payload=payload)
#         fresh_text = r.call_fresh()
#         resp = Response(fresh_text)
#         resp.run()
#         time.sleep(3)
