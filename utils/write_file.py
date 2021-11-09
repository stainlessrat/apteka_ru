import csv
import re

from utils.logger import Logger
from utils.medicines_codes import MedicineCodeHandler
from params import config

med_fdb = MedicineCodeHandler(config.PATH_MEDICINES_CODES)


class WriteFile(object):
    def __init__(self, name_out_file, name_logger):
        self.__name_out_file = name_out_file
        self.__log = Logger(name_logger)

    def write_medicine_data_to_csv(self, medicine, url, medicines_fdb):
        try:
            with open(self.__name_out_file, 'a', newline='') as f:
                spam_writer = csv.writer(f, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for med in medicine:
                    # для того, чтобы не записывать лекарственные средства без цены
                    price = med['price']
                    if price > 0:
                        spam_writer.writerow(
                            (self._get_medicine_code_fdb(med['name'].replace('&quot;', ''), medicines_fdb),
                             med['name'].replace('&quot;', ''),
                             med['vendor'].replace('&quot;', ''),
                             str(price).replace('.', ','),
                             url))
                    self.__log.write_log(f'[-] Error -1.2: Price is 0')
            self.__log.write_log(f'[+] File is successfully writed')
        except Exception as ex:
            self.__log.write_log(f'[-] Error -1.1: File not writed - ' + str(ex))

    def write_medicine_description_to_csv(self, medicine, url, medicines_fdb):
        try:
            with open(self.__name_out_file, 'a', newline='') as f:
                spam_writer = csv.writer(f, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                print("6 " + re.sub('\n|\r', ' ', medicine['pharm_kin']))
                medicine_code_id = self._get_medicine_code_fdb(re.sub('\n|\r', ' ', medicine['name']), medicines_fdb)
                if medicine_code_id:
                    spam_writer.writerow((url,
                                          medicine_code_id,
                                          re.sub('\n|\r', ' ', medicine['name']),
                                          re.sub('\n|\r', ' ', medicine['vendor']),
                                          re.sub('\n|\r', ' ', medicine['country']),
                                          re.sub('\n|\r', ' ', medicine['cautions']).replace(';', '.'),
                                          re.sub('\n|\r', ' ', medicine['gen_desc']).replace(';', '.'),
                                          re.sub('\n|\r', ' ', medicine['pharm_kin']).replace(';', '.'),
                                          re.sub('\n|\r', ' ', medicine['pharm_dyn']).replace(';', '.'),
                                          re.sub('\n|\r', ' ', medicine['struct']).replace(';', '.'),
                                          re.sub('\n|\r', ' ', medicine['side_eff']).replace(';', '.'),
                                          re.sub('\n|\r', ' ', medicine['contra_indic']).replace(';', '.'),
                                          re.sub('\n|\r', ' ', medicine['drug_inter']).replace(';', '.'),
                                          re.sub('\n|\r', ' ', medicine['dosage']).replace(';', '.'),
                                          re.sub('\n|\r', ' ', medicine['release']).replace(';', '.'),
                                          re.sub('\n|\r', ' ', medicine['dos_desc']).replace(';', '.'),
                                          re.sub('\n|\r', ' ', medicine['indic']).replace(';', '.'),
                                          re.sub('\n|\r', ' ', medicine['overdose']).replace(';', '.')
                                          ))
            self.__log.write_log(f'[+] File is successfully writed')
        except Exception as ex:
            self.__log.write_log(f'[-] Error -1.1: File not writed - ' + str(ex))

    def _get_medicine_code_fdb(self, med_name, medicines_fdb):
        if medicines_fdb:
            return med_fdb.check_medicine(med_name, medicines_fdb)
        else:
            return

    def write_heading_medicine_description(self, file):
        try:
            with open(self.__name_out_file, 'a', newline='') as f:
                spam_writer = csv.writer(f, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spam_writer.writerow(file)
            self.__log.write_log(f'[+] File is successfully writed')
        except Exception as ex:
            self.__log.write_log(f'[-] Error -1.2: File not writed - ' + str(ex))
