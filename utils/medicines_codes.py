import csv
import fdb

from params import config
from utils.logger import Logger

log = Logger(config.name_log)


class MedicineCodeHandler(object):

    def __init__(self, name_out_file):
        self.__name_out_file = name_out_file

    def write_to_csv(self, medicines):
        try:
            with open(self.__name_out_file, 'a', newline='') as f:
                spam_writer = csv.writer(f, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for med in medicines:
                    for k, v in med.items():
                        spam_writer.writerow((k, v))
            log.write_log(f'[+] File is successfully writed')
        except Exception as ex:
            log.write_log(f'[-] Error -6.2: File not writed - ' + str(ex))

    def read_from_csv(self, name_in_file):
        medicines = []
        try:
            with open(name_in_file) as f:
                reader = csv.reader(f, delimiter=';')
                for row in reader:
                    medicines.append({row[0]: row[1]})
        except Exception as ex:
            log.write_log(f'[-] Error -6.1: File not writed - ' + str(ex))
        finally:
            return medicines

    def get_medicine_fdb(self):
        for i in range(0, 3):
            try:
                con = fdb.connect(host=config.host_frb,
                                  database=config.path_database_frb,
                                  user=config.user_frb,
                                  password=config.password_frb,
                                  charset=config.charset_frb)
                cur = con.cursor()

                cur.execute(
                    'select em.emed_name, em.ext_code from plitem pi inner join ext_medicine em on pi.ext_code = em.ext_code and em.codetype = 3102 where pi.plid = 6')
                medicines = []
                for med, id in cur.fetchall():
                    medicines.append({med: id})
                return medicines
            except Exception as e:
                print(f'[-] Error -6.3: Exeption = ' + str(e))
                log.write_log(f'[-] Error -5.1: File not writed - ' + str(e))

    def check_medicine(self, name='', medicines=[]):
        for medicine in medicines:
            for k, v in medicine.items():
                if name == k:
                    return v
