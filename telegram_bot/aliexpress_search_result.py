class AliExpressSearchResult:
    def __init__(self, response_data, count):
        self.response_data = response_data
        self.result = response_data.get('result', {})
        self.status = self.result.get('status', {})
        self.settings = self.result.get('settings', {})
        self.base = self.result.get('base', {})
        self.result_list = self.result.get('resultList', [])[0:count + 1]

    def get_total_results(self):
        return self.base.get('totalResults', {})

    def get_items(self):
        items = []
        for result_item in self.result_list:
            item_data = result_item['item']
            item = {
                "itemId": item_data['itemId'],
                "title": item_data['title'],
                "sales": item_data['sales'],
                "itemUrl": item_data['itemUrl'],
                "image": item_data['image'],
                "price": item_data['sku']['def'].get('price', 0),
                "promotionPrice": item_data['sku']['def']['promotionPrice'],
                "averageStarRate": item_data['averageStarRate'],
                "type": item_data['type']
            }
            items.append(item)
        return items

    def get_status_code(self):
        return self.status['code']

    def get_status_message(self):
        return self.status['data']

    def get_request_time(self):
        return self.status['requestTime']


