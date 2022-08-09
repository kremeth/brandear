import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
from datetime import datetime, timedelta
from ebaysdk.trading import Connection as Trading
from tqdm import tqdm
import itertools
import numpy as np
import pandas as pd
from ebaysdk.shopping import Connection as Shopping
import flask
import os


app = flask.Flask(__name__)



# APP_ID = 'MathieuK-brandear-PRD-c13e2103b-cda61bfa'

# token_id = 'v^1.1#i^1#I^3#r^0#p^3#f^0#t^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'

# def get_results(payload):
#     days = 2
#     start = datetime.today()
#     while start >= datetime.today() - timedelta(days=30):
#         end = start - timedelta(days=days)
#         try:
#             # api = Connection(appid=APP_ID, config_file=None, devid='3b233cb3-45cb-4f15-befe-3843b07826e9', certid='PRD-13e2103b8ab5-5e97-4157-a0d0-c671', token=token_id)
#             api = Connection(appid=APP_ID, config_file=None, devid='3b233cb3-45cb-4f15-befe-3843b07826e9', certid='3b233cb3-45cb-4f15-befe-3843b07826e9')
#             # response = api.execute('findItemsAdvanced', {'StartTimeFrom': start,'StartTimeTo': end}, payload)
#             response = api.execute('FindItemsIneBayStores', payload)

#             # assert(response.reply.ack == 'Success')
#             # assert(type(response.reply.timestamp) == datetime.datetime)
#             # assert(type(response.reply.searchResult.item) == list)

#             return response.dict()
#             # assert(type(item.listingInfo.endTime) == datetime.datetime)
#             # assert(type(response.dict()) == dict)

#         except ConnectionError as e:
#             print(e)
#             print(e.response.dict())
#         start = end

# payload = {
#     'storeName': 'Brandear',
#     "paginationInput": { "pageNumber": "1" }
# }


# 'Auth LOUIS VUITTON Geronimos N51994 Ebene Damier CA0064 Bum Bag'



# api.execute('findItemsIneBayStores', payload).dict()['searchResult']['item'][0]




class Brandear:
    def __init__(self):
        self.APP_ID = 'MathieuK-brandear-PRD-c13e2103b-cda61bfa'
        self.token_id = 'v^1.1#i^1#I^3#r^0#p^3#f^0#t^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'
        self.devid = '3b233cb3-45cb-4f15-befe-3843b07826e9'
        self.certid='3b233cb3-45cb-4f15-befe-3843b07826e9'
        self.api = Connection(appid=self.APP_ID, config_file=None, devid=self.devid, certid=self.certid)
    def get_total_pages(self):
        request = {
            'storeName': 'Brandear',
        }
        return int(self.api.execute('findItemsIneBayStores', request).dict()['paginationOutput']['totalPages'])

    def get_items(self):
        self.items = []
        for i in tqdm(range(1, 101)):
            request = {
                "storeName": "Brandear",
                "paginationInput": { "pageNumber": f"{i}" }
            }
            page_items = self.api.execute('findItemsIneBayStores', request).dict()['searchResult']['item']
            self.items.append(page_items)

    def __call__(self):
        self.total_pages = self.get_total_pages()
        self.get_items()
        return self.items


@app.route('/')
@app.route('/home')
def home():
    return "waiting"


@app.route('/items')
def get_items():
    items = Brandear()()
    items = list(itertools.chain.from_iterable(items))

    item_id = np.array([val['itemId'] for val in items])
    item_title = np.array([val['title'] for val in items])
    item_image = np.array([val['galleryURL'] for val in items])
    item_category = np.array([val['primaryCategory']['categoryName'] for val in items])
    item_price = np.array([float(val['sellingStatus']['convertedCurrentPrice']['value']) for val in items])
    item_currency = np.array([val['sellingStatus']['convertedCurrentPrice']['_currencyId'] for val in items])
    item_url = np.array([val['viewItemURL'] for val in items])

    data = pd.DataFrame(columns=['item_id', 'item_title', 'item_image', 'item_category', 'item_price', 'item_currency', 'item_url'])
    data['item_id'] = item_id
    data['item_title'] = item_title
    data['item_image'] = item_image
    data['item_category'] = item_category
    data['item_price'] = item_price
    data['item_currency'] = item_currency
    data['item_url'] = item_url

    # Filter by price (less than 400 sgd) and by category
    data = data[data['item_price'] < 400/1.4][data['item_category'] == "Women's Bags & Handbags"]
    data.reset_index(inplace=True, drop=True)

    # data2 = [data.columns.values.tolist()]
    # data2.extend(data.values.tolist())
    # value_range_body = {"values": data2}

    # value_range_body = {
    #     "majorDimension":"COLUMNS",
    #     "values":
    #         [data2]
    #     }



    return data.to_json()


# APP_ID = 'MathieuK-brandear-PRD-c13e2103b-cda61bfa'
# token_id = 'v^1.1#i^1#I^3#r^0#p^3#f^0#t^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'
# devid = '3b233cb3-45cb-4f15-befe-3843b07826e9'
# certid='3b233cb3-45cb-4f15-befe-3843b07826e9'
# api = Connection(appid=APP_ID, config_file=None, devid=devid, certid=certid)

# request = {
#     "storeName": "Brandear",
#     "paginationInput": { "pageNumber": "101" },
#     "itemFilter": [
#       {
#         "name": "ModTimeFrom",
#         "value": f"{(datetime.today() - timedelta(days=2)).isoformat()}",
#       }
#     ]
# }
# api.execute('findItemsIneBayStores', request).dict()['searchResult']['item']



if __name__ == "__main__":
    app.secret_key = 'ItIsASecret'
    # app.debug = True
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))




                   
                   
                   


