from params import config
from utils.logger import Logger

log = Logger(config.name_log)


class DataFromJson(object):
    def __init__(self):
        self.result = []

    def get_data_from_json(self, data_json):
        try:
            variant = data_json['groupItems']
            self._get_data(variant)
            return self.result
        except Exception as ex:
            log.write_log(f'[-] Error -30.1: {ex}')
            print(f'[-] Error -30.1: {ex}')

    def _get_data(self, variant):
        print(variant)
        for child in variant:
            if child:
                for item in child.get('itemInfos'):
                    self.result.append(self._get_info(item))

    def _get_info(self, item):
        res = {}
        try:
            res['name'] = item['name']
            res['vendor'] = item['vendor']
            res['price'] = item['price']
        except Exception as ex:
            log.write_log(f'[-] Error -30: {ex}')
            print(f'[-] Error -30: {ex}')
        print(res)
        return res
