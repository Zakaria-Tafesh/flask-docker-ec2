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

        # if self.render_page:
        #     res = request_html()
        # else:
        #     res = request_normal()

        res = request_normal()
        logger.info(res.text)
        return res.status_code

    @staticmethod
    def decode_response(response):
        logger.info(response.status_code)
        if response.status_code < 300:
            logger.info(response.text[:100])
            logger.info('#'*100)
            logger.info(response.content[:100])
            logger.info('#'*100)
            decoded_text = response.content.decode('utf-8')  # Assuming it's UTF-8 encoded text
            logger.info(decoded_text[:100])
            return decoded_text

    def call_map(self):
        logger.info('call_map')
        self.update_params()
        # self.headers = {'authority': 'www.torontopropertyhunters.com', 'method': 'POST', 'path': '/property-search/res/includes/search_application/get_listings_for_map.asp', 'scheme': 'https', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.9,ar-AE;q=0.8,ar;q=0.7', 'Cache-Control': 'no-cache', 'Content-Type': 'application/x-www-form-urlencoded', 'Origin': 'https://www.torontopropertyhunters.com', 'Referer': 'https://www.torontopropertyhunters.com/property-search/results/', 'User-Agent ': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36', 'X-Kl-Ajax-Request': 'Ajax_Request', 'X-Requested-With': 'XMLHttpRequest'}
        # self.payload = '''searchParameters=%7B%22searchType%22%3A%22map%22%2C%22adminUserId%22%3A-1%2C%22clientSearch%22%3A%7B%22id%22%3A%229516219%22%2C%22active%22%3Afalse%2C%22type%22%3A1%2C%22featuredFirst%22%3Afalse%7D%2C%22favorite%22%3Afalse%2C%22mlsRegionId%22%3A211%2C%22mlsRegions%22%3A%22211%22%2C%22listingClass%22%3A-1%2C%22listingStatus%22%3A%22Active%22%2C%22quickSearch%22%3A%7B%22mls%22%3A%22%22%2C%22type%22%3A-1%7D%2C%22search%22%3A%7B%22acreage%22%3A%7B%22max%22%3A%22%22%2C%22min%22%3A%22%22%7D%2C%22age%22%3A%7B%22min%22%3A0%7D%2C%22baths%22%3A%7B%22max%22%3A100%2C%22min%22%3A%22%22%7D%2C%22beds%22%3A%7B%22max%22%3A100%2C%22min%22%3A%22%22%7D%2C%22daysOnMarket%22%3A1%2C%22extra%22%3A%7B%22basement%22%3A%22%22%2C%22construction%22%3A%22%22%2C%22energy%22%3A%22%22%2C%22exterior%22%3A%22%22%2C%22fencing%22%3A%22%22%2C%22interior%22%3A%22%22%2C%22lots%22%3A%22%22%2C%22owner%22%3A%22%22%2C%22stories%22%3A%22%22%2C%22styles%22%3A%22%22%2C%22searchFeatures%22%3A%22%22%7D%2C%22filter%22%3A%7B%22excludeMLSIds%22%3A%22%22%2C%22includeAgentIds%22%3A%22%22%2C%22includeMLSIds%22%3A%22%22%2C%22includeOfficeIds%22%3A%22%22%7D%2C%22flags%22%3A%7B%22acrossStreetFromOcean%22%3Afalse%2C%22bayFront%22%3Afalse%2C%22beachfront%22%3Afalse%2C%22equestrian%22%3Afalse%2C%22foreclosure%22%3Afalse%2C%22golfCourseFront%22%3Afalse%2C%22gulfFront%22%3Afalse%2C%22hdPhotos%22%3Afalse%2C%22hudHome%22%3Afalse%2C%22mbOnFirstFloor%22%3Afalse%2C%22newConstruction%22%3Afalse%2C%22oceanFront%22%3Afalse%2C%22openHouse%22%3Afalse%2C%22pool%22%3Afalse%2C%22reo%22%3Afalse%2C%22shortSale%22%3Afalse%2C%22singleLevel%22%3Afalse%2C%22spa%22%3Afalse%2C%22viewScenic%22%3Afalse%2C%22virtualTour%22%3Afalse%2C%22waterFront%22%3Afalse%2C%22woodedLot%22%3Afalse%2C%22hasPhoto%22%3Afalse%7D%2C%22garageCap%22%3A%7B%22min%22%3A%22%22%7D%2C%22hoaFees%22%3A%7B%22max%22%3A%22%22%2C%22min%22%3A%22%22%7D%2C%22supportedListTypes%22%3A%221%2C2%2C3%2C8%22%2C%22listType%22%3A%221%2C2%22%2C%22listTypeDescrip%22%3A%22%22%2C%22location%22%3A%7B%22areas%22%3A%22%22%2C%22cities%22%3A%22%22%2C%22condoProjectNames%22%3A%22%22%2C%22counties%22%3A%22%22%2C%22schools%22%3A%22%22%2C%22states%22%3A%22%22%2C%22subAreas%22%3A%22%22%2C%22subDivisions%22%3A%22%22%2C%22address%22%3A%22%22%2C%22townships%22%3A%22%22%2C%22zips%22%3A%22%22%2C%22elementarySchools%22%3A%22%22%2C%22middleSchools%22%3A%22%22%2C%22highSchools%22%3A%22%22%2C%22juniorHighSchools%22%3A%22%22%7D%2C%22map%22%3A%7B%22eastLong%22%3A-79.15863671880732%2C%22northLat%22%3A43.72638914799237%2C%22searchRegion%22%3A%22POLYGON((-79.2755903612793+43.668684216434805%2C-79.2862333666504+43.69252018662192%2C-79.36142104975586+43.67538904018543%2C-79.38682693354492+43.73693904868733%2C-79.4184126269043+43.72999301911968%2C-79.41188949458008+43.71560225218159%2C-79.4290556322754+43.711879939507895%2C-79.42699569575196+43.70542738317693%2C-79.51248306147461+43.68730687732119%2C-79.51797622553711+43.697981262718514%2C-79.5450987230957+43.71138361368261%2C-79.58938735834961+43.668684216434805%2C-79.59350723139649+43.660240039524744%2C-79.61273330561524+43.64185743101185%2C-79.59316390864258+43.644093454203855%2C-79.58526748530274+43.63589429562705%2C-79.58080428950196+43.62669996910205%2C-79.56535476557617+43.624960343696344%2C-79.53857559077149+43.58070723858497%2C-79.5117964159668+43.57921499377228%2C-79.47677749506836+43.60383230370679%2C-79.31816238276367+43.60805850554636%2C-79.2755903612793+43.668684216434805))%22%2C%22southLat%22%3A43.56587940418003%2C%22westLong%22%3A-79.7118341648841%2C%22centerLat%22%3A43.646205177467714%2C%22centerLong%22%3A-79.4352354418457%2C%22zoomLevel%22%3A12%2C%22nearby%22%3Afalse%2C%22radius%22%3A-1%7D%2C%22alert%22%3A%7B%22startDate%22%3A%22%22%2C%22priceChangeDate%22%3A%22%22%7D%2C%22price%22%3A%7B%22max%22%3A%22%22%2C%22min%22%3A%22%22%7D%2C%22priceReductionPercentage%22%3A%22%22%2C%22soldDays%22%3A%22%22%2C%22openHouseDays%22%3A0%2C%22openHouseType%22%3A0%2C%22priceChangeDays%22%3A%22%22%2C%22sortBy%22%3A%22m.DateListed+DESC%22%2C%22sqft%22%3A%7B%22max%22%3A%22%22%2C%22min%22%3A%22%22%7D%2C%22lotSizeSqft%22%3A%7B%22max%22%3A1000000%2C%22min%22%3A%22%22%7D%2C%22yearBuilt%22%3A%7B%22max%22%3A%22%22%2C%22min%22%3A%22%22%7D%2C%22offset%22%3A%7B%22pageSize%22%3A12%2C%22pageNumber%22%3A1%2C%22listingId%22%3A%22%22%7D%2C%22statusActivityDays%22%3A%22%22%2C%22photos%22%3A%7B%22max%22%3A%22%22%2C%22min%22%3A%22%22%7D%7D%2C%22searchId%22%3A-1%2C%22activeId%22%3A1%2C%22userId%22%3A%22%22%7D'''
        # self.payload = '''searchParameters=%7B%22searchType%22%3A%22map%22%2C%22adminUserId%22%3A-1%2C%22clientSearch%22%3A%7B%22id%22%3A%229516219%22%2C%22active%22%3Afalse%2C%22type%22%3A1%2C%22featuredFirst%22%3Afalse%7D%2C%22favorite%22%3Afalse%2C%22mlsRegionId%22%3A211%2C%22mlsRegions%22%3A%22211%22%2C%22listingClass%22%3A-1%2C%22listingStatus%22%3A%22Active%22%2C%22quickSearch%22%3A%7B%22mls%22%3A%22%22%2C%22type%22%3A-1%7D%2C%22search%22%3A%7B%22acreage%22%3A%7B%22max%22%3A%22%22%2C%22min%22%3A%22%22%7D%2C%22age%22%3A%7B%22min%22%3A0%7D%2C%22baths%22%3A%7B%22max%22%3A100%2C%22min%22%3A%22%22%7D%2C%22beds%22%3A%7B%22max%22%3A100%2C%22min%22%3A%22%22%7D%2C%22daysOnMarket%22%3A1%2C%22extra%22%3A%7B%22basement%22%3A%22%22%2C%22construction%22%3A%22%22%2C%22energy%22%3A%22%22%2C%22exterior%22%3A%22%22%2C%22fencing%22%3A%22%22%2C%22interior%22%3A%22%22%2C%22lots%22%3A%22%22%2C%22owner%22%3A%22%22%2C%22stories%22%3A%22%22%2C%22styles%22%3A%22%22%2C%22searchFeatures%22%3A%22%22%7D%2C%22filter%22%3A%7B%22excludeMLSIds%22%3A%22%22%2C%22includeAgentIds%22%3A%22%22%2C%22includeMLSIds%22%3A%22%22%2C%22includeOfficeIds%22%3A%22%22%7D%2C%22flags%22%3A%7B%22acrossStreetFromOcean%22%3Afalse%2C%22bayFront%22%3Afalse%2C%22beachfront%22%3Afalse%2C%22equestrian%22%3Afalse%2C%22foreclosure%22%3Afalse%2C%22golfCourseFront%22%3Afalse%2C%22gulfFront%22%3Afalse%2C%22hdPhotos%22%3Afalse%2C%22hudHome%22%3Afalse%2C%22mbOnFirstFloor%22%3Afalse%2C%22newConstruction%22%3Afalse%2C%22oceanFront%22%3Afalse%2C%22openHouse%22%3Afalse%2C%22pool%22%3Afalse%2C%22reo%22%3Afalse%2C%22shortSale%22%3Afalse%2C%22singleLevel%22%3Afalse%2C%22spa%22%3Afalse%2C%22viewScenic%22%3Afalse%2C%22virtualTour%22%3Afalse%2C%22waterFront%22%3Afalse%2C%22woodedLot%22%3Afalse%2C%22hasPhoto%22%3Afalse%7D%2C%22garageCap%22%3A%7B%22min%22%3A%22%22%7D%2C%22hoaFees%22%3A%7B%22max%22%3A%22%22%2C%22min%22%3A%22%22%7D%2C%22supportedListTypes%22%3A%221%2C2%2C3%2C8%22%2C%22listType%22%3A%221%2C2%22%2C%22listTypeDescrip%22%3A%22%22%2C%22location%22%3A%7B%22areas%22%3A%22%22%2C%22cities%22%3A%22%22%2C%22condoProjectNames%22%3A%22%22%2C%22counties%22%3A%22%22%2C%22schools%22%3A%22%22%2C%22states%22%3A%22%22%2C%22subAreas%22%3A%22%22%2C%22subDivisions%22%3A%22%22%2C%22address%22%3A%22%22%2C%22townships%22%3A%22%22%2C%22zips%22%3A%22%22%2C%22elementarySchools%22%3A%22%22%2C%22middleSchools%22%3A%22%22%2C%22highSchools%22%3A%22%22%2C%22juniorHighSchools%22%3A%22%22%7D%2C%22map%22%3A%7B%22eastLong%22%3A-79.12705102544794%2C%22northLat%22%3A43.72643910790157%2C%22searchRegion%22%3A%22POLYGON((-79.2755903612793+43.668684216434805%2C-79.2862333666504+43.69252018662192%2C-79.36142104975586+43.67538904018543%2C-79.38682693354492+43.73693904868733%2C-79.4184126269043+43.72999301911968%2C-79.41188949458008+43.71560225218159%2C-79.4290556322754+43.711879939507895%2C-79.42699569575196+43.70542738317693%2C-79.51248306147461+43.68730687732119%2C-79.51797622553711+43.697981262718514%2C-79.5450987230957+43.71138361368261%2C-79.58938735834961+43.668684216434805%2C-79.59350723139649+43.660240039524744%2C-79.61273330561524+43.64185743101185%2C-79.59316390864258+43.644093454203855%2C-79.58526748530274+43.63589429562705%2C-79.58080428950196+43.62669996910205%2C-79.56535476557617+43.624960343696344%2C-79.53857559077149+43.58070723858497%2C-79.5117964159668+43.57921499377228%2C-79.47677749506836+43.60383230370679%2C-79.31816238276367+43.60805850554636%2C-79.2755903612793+43.668684216434805))%22%2C%22southLat%22%3A43.54840522841218%2C%22westLong%22%3A-79.68024847152472%2C%22centerLat%22%3A43.63750936989681%2C%22centerLong%22%3A-79.40364974848633%2C%22zoomLevel%22%3A12%2C%22nearby%22%3Afalse%2C%22radius%22%3A-1%7D%2C%22alert%22%3A%7B%22startDate%22%3A%22%22%2C%22priceChangeDate%22%3A%22%22%7D%2C%22price%22%3A%7B%22max%22%3A%22%22%2C%22min%22%3A%22%22%7D%2C%22priceReductionPercentage%22%3A%22%22%2C%22soldDays%22%3A%22%22%2C%22openHouseDays%22%3A0%2C%22openHouseType%22%3A0%2C%22priceChangeDays%22%3A%22%22%2C%22sortBy%22%3A%22m.DateListed+DESC%22%2C%22sqft%22%3A%7B%22max%22%3A%22%22%2C%22min%22%3A%22%22%7D%2C%22lotSizeSqft%22%3A%7B%22max%22%3A1000000%2C%22min%22%3A%22%22%7D%2C%22yearBuilt%22%3A%7B%22max%22%3A%22%22%2C%22min%22%3A%22%22%7D%2C%22offset%22%3A%7B%22pageSize%22%3A12%2C%22pageNumber%22%3A1%2C%22listingId%22%3A%22%22%7D%2C%22statusActivityDays%22%3A%22%22%2C%22photos%22%3A%7B%22max%22%3A%22%22%2C%22min%22%3A%22%22%7D%7D%2C%22searchId%22%3A-1%2C%22activeId%22%3A1%2C%22userId%22%3A%22%22%7D'''
        # self.api_map = 'https://www.torontopropertyhunters.com/property-search/res/includes/search_application/get_listings_for_map.asp'
        logger.info(f'self.api_map {self.api_map}')
        logger.info(f'self.headers {self.headers}')
        logger.info(f'self.payload {self.payload}')

        response = requests.post(self.api_map, data=self.payload, headers=self.headers, params={"": ""})

        return self.decode_response(response)
        # if response.status_code == 200:
        #     resp_text = response.text
        #     logger.info(resp_text[:100])
        #     return resp_text


# if __name__ == "__main__":
#     for client in clients_list:
#         payload = client['payload_fresh_map']
#         name = client['client_name']
#         r = Request(payload=payload)
#         fresh_text = r.call_fresh()
#         resp = Response(fresh_text)
#         resp.run()
#         time.sleep(3)
