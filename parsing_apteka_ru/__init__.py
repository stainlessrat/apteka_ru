import random
import shutil
import time
import re

from selenium import webdriver
from datetime import datetime

from params import config
from parsing_apteka_ru.data_from_json import DataFromJson
from parsing_apteka_ru.json_from_api_apteka import ApiAptekaRu
from utils.logger import Logger
from utils.medicines_codes import MedicineCodeHandler
from utils.move_on_ftp import FtpParsing
from utils.write_file import WriteFile

log = Logger(config.name_log)
med_fdb = MedicineCodeHandler(config.PATH_MEDICINES_CODES)


class ParsingAptekaRu(object):

    def __init__(self):
        """
        Whenever instance is init we will open connection
        """
        self._driver = webdriver.Chrome()

        self.medicines_fdb = med_fdb.get_medicine_fdb()
        if self.medicines_fdb:
            med_fdb.write_to_csv(self.medicines_fdb)
            self._name_out_file = './' + self._get_name_out_file() + '_apteka_ru.csv'
        else:
            self.medicines_fdb = med_fdb.read_from_csv(config.PATH_MEDICINES_CODES)
            self._name_out_file = './' + self._get_name_out_file() + '_apteka_ru_F.csv'

        self._write = WriteFile(self._name_out_file, config.name_log)

    def __del__(self):
        """
        Whenever instance is deleted we will close connection
        :return: None
        """
        self._driver.quit()

    def start(self):
        log.write_log('[+] Start parsing')
        alphabet_links = self._get_links(config.SITE_NAME_APTEKA_RU, 'alphabet')
        if alphabet_links:
            for alphabet_link in alphabet_links:
                char_links = self._get_links(alphabet_link, 'medicinesPage__list')
                if char_links:
                    for char_link in char_links:
                        log.write_log(f'[+] {char_link}')
                        print(f'[+] {char_link}')
                        code_medicines = self._get_code_medicine(char_link)
                        if code_medicines:
                            for code in code_medicines:
                                log.write_log(f'[+] {code}')
                                print(f'[+] {code}')
                                json_apteka = ApiAptekaRu()
                                url_api = f'https://api.apteka.ru/Item/GroupInfo?itemGroupId={code}&cityId=5e57858e2b690a0001b0977f'
                                try:
                                    data_json = json_apteka.get_api_json(url_api)
                                    if data_json:
                                        data_medicine = DataFromJson()
                                        medicine = data_medicine.get_data_from_json(data_json)
                                        if medicine:
                                            self._write.write_medicine_data_to_csv(medicine, char_link,
                                                                                   self.medicines_fdb)
                                        else:
                                            log.write_log('[-] Error -5: data_medicine is None')
                                            print('[-] Error -5: data_medicine is None')
                                    else:
                                        log.write_log('[-] Error -4: data_json is None')
                                        print('[-] Error -4: data_json is None')
                                except Exception as e:
                                    log.write_log(f'[-] Error -77: json is break: {e}')
                                    print(f'[-] Error -77: json is break: {e}')
                            else:
                                log.write_log('[+] All medicine\'s codes got. Successfully.')
                                print('[+] All medicine\'s codes got. Successfully.')
                        else:
                            log.write_log('[-] Error -3: code_medicines is None')
                            print('[-] Error -3: code_medicines is None')
                    else:
                        log.write_log('[+] All chars\' links end. Successfully.')
                        print('[+] All chars\' links end. Successfully.')
                else:
                    log.write_log('[-] Error -2: char_links is None')
                    print('[-] Error -2: char_links is None')
            else:
                log.write_log('[+] All alphabet\'s links end. Successfully.')
                print('[+] All alphabet\'s links end. Successfully.')
        else:
            log.write_log('[-] Error -1: alphabet_links is None')
            print('[-] Error -1: alphabet_links is None')
        self._copy_csv(self._name_out_file)
        self._move_ftp(self._name_out_file)
        log.write_log('[+] Stop parsing')

    def _get_links(self, url, name_class):
        """
        For getting alphabet links from main page site
        :param url: string url
        :param name_class: string class div
        :return: list of alphabet links
        """
        time.sleep(random.random())
        links = []
        for i in range(0, 3):
            try:
                self._driver.get(url)
                self._driver.minimize_window()

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
        """
        For getting medicine's codes for api requests
        :param url: string url from medicine list
        :return: string medicine's codes
        """
        time.sleep(random.random())
        codes = []
        for i in range(0, 3):
            try:
                self._driver.get(url)
                self._driver.minimize_window()

                result = self._driver.find_element_by_class_name('ViewPreparation__items')
                a_class = result.find_elements_by_class_name('card-flex')
                if a_class:
                    for a in a_class:
                        codes.append(re.search(r'[a-z0-9]+/$', a.get_attribute('href')).group(0).strip('/'))
                return codes
            except Exception as ex:
                log.write_log(f'[-] Error -21: {ex}')
                print(f'[-] Error -21: {ex}')
                time.sleep(2)

    def _get_name_out_file(self):
        return datetime.now().strftime("%d%m%Y")

    def _copy_csv(self, file_csv=''):
        """
        For copy parsing file on FILE-2 disk
        :param file_csv: Name parsing file in format .csv
        :return: None
        """
        file_copy = f'\\\\Parsing\\APTEKA.RU\\100SKU\\' + datetime.now().strftime(
            "%d%m%Y_%H") + "00.csv"
        try:
            shutil.copyfile(file_csv, file_copy)
            log.write_log('[+] File is successfully move')
        except Exception as ex:
            log.write_log('Error: ' + str(ex))

    def _move_ftp(self, file_csv=''):
        """
        For copy parsing file on Agrores FTP
        :param file_csv: Name parsing file in format .csv
        :return: None
        """
        move_ftp = FtpParsing(config.HOST_FTP, config.PORT_FTP, config.LOGIN_FTP, config.PASSWORD_FTP)
        try:
            move_ftp.copy_file(file_csv)
            log.write_log('[+] File is succefully copy in ftp')
        except Exception as ex:
            log.write_log('Error: ftp - ' + str(ex))
