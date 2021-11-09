import random
import re
import time

from selenium import webdriver

from params import config
from parsing_apteka_ru import ApiAptekaRu
from utils.logger import Logger
from utils.medicines_codes import MedicineCodeHandler
from utils.write_file import WriteFile

log = Logger(config.medicines_description_name_log)
med_fdb = MedicineCodeHandler(config.PATH_MEDICINES_CODES)


class MedicinesDescription(object):

    def __init__(self):
        self._driver = webdriver.Chrome()
        self._write = WriteFile('descriptions_apteka_ru.csv', config.medicines_description_name_log)

        self.medicines_fdb = med_fdb.get_medicine_fdb()

        if self.medicines_fdb:
            med_fdb.write_to_csv(self.medicines_fdb)
        else:
            self.medicines_fdb = med_fdb.read_from_csv(config.PATH_MEDICINES_CODES)

    def __del__(self):
        if self._driver:
            self._driver.quit()

    def start(self):
        log.write_log('[+] Start parsing')

        self._write.write_heading_medicine_description(config.heading_output_file)

        alphabet_links = self._get_links(config.SITE_NAME_APTEKA_RU, 'alphabet')

        if alphabet_links:
            for alphabet_link in alphabet_links:
                char_links = self._get_links(alphabet_link, 'medicinesPage__list')
                if char_links:
                    for char_link in char_links:
                        code_medicines = self._get_code_medicine(char_link)
                        print(code_medicines)
                        if code_medicines:
                            for code in code_medicines:
                                json_apteka = ApiAptekaRu()
                                url_info = f'https://api.apteka.ru/Item/Info?id={code}&cityId=5e57858e2b690a0001b0977f'
                                data_json_info = json_apteka.get_api_json(url_info)
                                if data_json_info:
                                    data_medicines_description = self._get_data_from_json(data_json_info)
                                    if data_medicines_description:
                                        print(data_medicines_description)
                                        self._write.write_medicine_description_to_csv(data_medicines_description,
                                                                                      char_link,
                                                                                      self.medicines_fdb)
                                    else:
                                        log.write_log('[-] Данных о лекарственных средствах не получены')
                                else:
                                    log.write_log('[+] Все данные о лекарственных средствах получены успешно')
                            else:
                                log.write_log('[+] Все коды лекарств пройдены успешно')
                        else:
                            log.write_log('[-] Коды лекарств не найдены')
                    else:
                        log.write_log('[+] Ссылки с буквы пройдены успешно')
                else:
                    log.write_log('[-] Ссылки на букву не найдены')
            else:
                log.write_log('[+] Все ссылки с блока Список лекарств по алфавиту пройдены успешно')
                print('[+] Все ссылки с блока Список лекарств по алфавиту пройдены успешно')
        else:
            log.write_log('[-] Error -1: Ссылки с алфавитного списка не получены')
            print('[-] Error -1: Ссылки с алфавитного списка не получены')
        log.write_log('[+] Stop parsing')

    def _get_links(self, url, name_class):
        time.sleep(random.random())

        links = []

        for i in range(0, 3):
            try:
                self._driver.get(url)

                result = self._driver.find_element_by_class_name(name_class)

                list_a = result.find_elements_by_tag_name('a')
                for a in list_a:
                    links.append(a.get_attribute('href'))
                return links
            except Exception as ex:
                log.write_log(f'[-] Error -20: {ex}')
                print(f'[-] Error -20: {ex}')

                time.sleep(2)

    def _get_code_medicine(self, url):
        time.sleep(random.random())
        codes = []
        for i in range(0, 3):
            try:
                self._driver.get(url)
                self._driver.minimize_window()

                result = self._driver.find_element_by_class_name('ViewPreparation__items')
                a_class = result.find_elements_by_class_name('CategoryItemCard__title')
                if a_class:
                    for a in a_class:
                        codes.append(re.search(r'[a-z0-9]+/$', a.get_attribute('href')).group(0).strip('/'))
                return codes
            except Exception as ex:
                log.write_log(f'[-] Error -21: {ex}')
                print(f'[-] Error -21: {ex}')
                time.sleep(2)

    def _get_data_from_json(self, data_json_info):
        res = {}
        try:
            res['name'] = data_json_info['name'] if data_json_info['name'] is not None else ''
            res['vendor'] = data_json_info['vendor'] if data_json_info['vendor'] is not None else ''
            res['country'] = data_json_info['country'] if data_json_info['country'] is not None else ''
            res['cautions'] = data_json_info['cautions'] if data_json_info['cautions'] is not None else ''
            res['gen_desc'] = data_json_info['genDesc'] if data_json_info['genDesc'] is not None else ''
            res['pharm_kin'] = data_json_info['pharmKin'] if data_json_info['pharmKin'] is not None else ''
            res['pharm_dyn'] = data_json_info['pharmDyn'] if data_json_info['pharmDyn'] is not None else ''
            res['struct'] = data_json_info['struct'] if data_json_info['struct'] is not None else ''
            res['side_eff'] = data_json_info['sideEff'] if data_json_info['sideEff'] is not None else ''
            res['contra_indic'] = data_json_info['contraIndic'] if data_json_info['contraIndic'] is not None else ''
            res['drug_inter'] = data_json_info['drugInter'] if data_json_info['drugInter'] is not None else ''
            res['dosage'] = data_json_info['dosage'] if data_json_info['dosage'] is not None else ''
            res['release'] = data_json_info['release'] if data_json_info['release'] is not None else ''
            res['dos_desc'] = data_json_info['dosDesc'] if data_json_info['dosDesc'] is not None else ''
            res['indic'] = data_json_info['indic'] if data_json_info['indic'] is not None else ''
            res['overdose'] = data_json_info['overdose'] if data_json_info['overdose'] is not None else ''

            return res

        except Exception as ex:
            log.write_log(f'[-] Error -30.1: {ex}')
            print(f'[-] Error -30.1: {ex}')
