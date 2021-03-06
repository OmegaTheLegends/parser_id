import threading
import time, os
import schedule
os.chdir('/opt/parser_id/')
#### Parsers
from ozon_api import start as oz
from aliexpress import main as ali
from wildberries import start as wb
from sbermegamarket import main as sb
from castorama import start as casto
from dns import main as dns_start
from citilink import main as citi

import logging
logging.basicConfig(level=logging.INFO)

logging.info('parser_id started')

def job_oz():
    try:
        logging.info("I'm running on thread OZON  %s" % threading.current_thread())
        oz()
        logging.info('Complite OZON')
    except Exception as Arg:
        logging.warning('error OZON' + f'\n {Arg}')

def job_wb():
    try:
        logging.info("I'm running on thread WB  %s" % threading.current_thread())
        wb()
        logging.info('Complite WB')
    except Exception as Arg:
        logging.warning('error WB' + f'\n {Arg}')

def job_sber():
    try:
        logging.info("I'm running on thread SBER  %s" % threading.current_thread())
        sb()
        logging.info('Complite SBER')
    except Exception as Arg:
        logging.warning('error SBER' + f'\n {Arg}')

def job_dns():
    try:
        logging.info("I'm running on thread DNS-SHOP  %s" % threading.current_thread())
        dns_start()
        logging.info('Complite DNS-SHOP')
    except Exception as Arg:
        logging.warning('error DNS-SHOP' + f'\n {Arg}')

def job_casto():
    try:
        logging.info("I'm running on thread Castorama  %s" % threading.current_thread())
        casto()
        logging.info('Complite Castorama')
    except Exception as Arg:
        logging.warning('error Castorama' + f'\n {Arg}')

def job_citi():
    try:
        logging.info("I'm running on thread Citilink  %s" % threading.current_thread())
        citi()
        logging.info('Complite Citilink')
    except Exception as Arg:
        logging.warning('error Citilink' + f'\n {Arg}')

def job_ali():
    try:
        logging.info("I'm running on thread Aliexpress  %s" % threading.current_thread())
        ali()
        logging.info('Complite Aliexpress')
    except Exception as Arg:
        logging.warning('error Aliexpress' + f'\n {Arg}')

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

schedule.every().day.at('00:01').do(run_threaded, job_wb)
schedule.every().day.at('01:05').do(run_threaded, job_oz)
schedule.every().day.at('01:30').do(run_threaded, job_sber)
schedule.every().day.at('02:00').do(run_threaded, job_dns)
schedule.every().day.at('02:30').do(run_threaded, job_ali)
schedule.every().day.at('03:01').do(run_threaded, job_casto)
schedule.every().day.at('03:20').do(run_threaded, job_citi)



while 1:
    schedule.run_pending()
    time.sleep(1)
