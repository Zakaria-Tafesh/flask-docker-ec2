import json
import time
import traceback

import requests
# from requests_html import HTMLSession
from dataclasses import dataclass
# from rich import print
from input.config import headers_fresh, api_fresh, api_fresh_map
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
    page_num: int = 1
    render_page: bool = False
    status_code: int = 400
    response_json: dict = None
    session: None = None
    api_fresh: str = api_fresh
    api_fresh_map: str = api_fresh_map

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

        if self.render_page:
            res = request_normal()
        else:
            res = request_normal()

        logger.info(res.text)
        return res.status_code

    def call_fresh(self):
        logger.info('call_fresh')
        # response = requests.request("POST", self.api_fresh_map, data=payload_fresh_map, headers=headers_fresh, params={"": ""})

        response = requests.post(self.api_fresh_map, data=self.payload, headers=headers_fresh, params={"": ""})
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
