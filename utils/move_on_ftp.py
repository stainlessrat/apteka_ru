from ftplib import FTP


class FtpParsing(object):

    def __init__(self, host='', port=0, login='', password=''):
        self._ftp = FTP()
        self._HOST = host
        self._PORT = port
        self._LOGIN = login
        self._PASSWORD = password

    def _connect(self):
        self._ftp.connect(self._HOST, self._PORT)
        self._ftp.login(self._LOGIN, self._PASSWORD)

    def _change_dir(self):
        self._connect()
        self._ftp.cwd('OUT')
        self._ftp.cwd('PARSING')

    def copy_file(self, path):
        self._connect()
        self._change_dir()
        with open(path, 'rb') as fobj:
            self._ftp.storbinary('STOR ' + path, fobj, 1024)
        self._close()

    def _close(self):
        self._ftp.quit()
