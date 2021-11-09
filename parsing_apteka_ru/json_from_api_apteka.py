import json
import random
import time
import requests

from utils.logger import Logger
from params import config

log = Logger(config.name_log)


class ApiAptekaRu(object):

    def __init__(self):
        pass

    def get_api_json(self, code):
        """

        :param code:
        :return:
        """
        log.write_log(code)
        print(code)
        url = self._get_html(code)
        try:
            j = json.loads(url)
            return j
        except Exception as e:
            print('Error j: ', e)
            return None

    def _get_html(self, url):
        for i in range(0, 3):
            time.sleep(random.random())
            try:
                r = requests.get(url)
                if r.ok:
                    log.write_log(f'[+] html got, status={r.status_code}')
                    print(f'[+] html got, status={r.status_code}')
                    return r.text
                else:
                    log.write_log(f'[-] Error -15: {str(r.status_code)}')
                    print(f'[-] Error -15: {str(r.status_code)}')
                    time.sleep(2)
            except Exception as e:
                log.write_log(f'[-] Error -14: {str(e)}')
                print(f'[-] Error -14: {str(e)}')
                time.sleep(2)
