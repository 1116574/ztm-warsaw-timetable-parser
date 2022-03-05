import ftplib
import datetime
import sys


def get_file():
    today = datetime.datetime.now()
    today = today.strftime('%y%m%d')

    ftp = ftplib.FTP('rozklady.ztm.waw.pl')
    ftp.login()

    with open('timetable.7z', 'wb') as fp:
        ftp.retrbinary(f'RETR RA{today}.7z', fp.write)

    ftp.quit()

    try:
        import py7zr
        with py7zr.SevenZipFile("timetable.7z", 'r') as archive:
            archive.extractall()
    except ImportError:
        print('py7zr not installed; Cannot unpack data')
        print('pip install py7zr')
        quit()

if __name__ == '__main__':
    get_file()