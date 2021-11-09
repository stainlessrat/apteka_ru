SITE_NAME_APTEKA_RU = 'https://apteka.ru/'

PATH_MEDICINES_CODES = './medicines_codes.csv'

name_log = 'apteka_'
medicines_description_name_log = 'med_description_'

# For connect FTP
HOST_FTP = '192.168.1.1'
PORT_FTP = 5555
LOGIN_FTP = 'login'
PASSWORD_FTP = 'password'

# For connect Firebird
host_frb = '192.168.1.2/4444'
path_database_frb = f'E:\path\file.FDB'
user_frb = 'login'
password_frb = 'password'
charset_frb = 'WIN1251'

# For head of output file
heading_output_file = (
        'URL - адрес',
        'Код лекарственного средства',
        'Наименование лекарственного средства',
        'Производитель',
        'Страна производителя',
        'Особые условия',
        'Общее описание',
        'Фармакинетика',
        'Фармадинамика',
        'Состав',
        'Побочные действия',
        'Противопоказания',
        'Лекарственное взаимодействие',
        'Дозировка',
        'Форма выпуска',
        'Лекарственная форма',
        'Показания к применению',
        'Передозировка',
)
