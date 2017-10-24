import time
import pandas
import requests
import logging
import os
import uuid
import lazy_logger
import diffhtml

from django.conf import settings
from collections import OrderedDict
from bs4 import BeautifulSoup
from radars.models import Archive
from markupsafe import Markup


logger = logging.getLogger(__name__)

cutoff = 0.6


def log_time():
    """return str time
    """
    return str(time.strftime("%Y%m%d%H%M", time.localtime(time.time())))


def get_log(file, title):
    with open(file, 'rb') as fp:
        logs = OrderedDict([(title, fp.read())])
    return logs


def order_fruit(fruit, num_fruit):
    time.sleep(num_fruit)
    return (
        '{fruit}_{num_fruit:d}'
        .format(fruit=fruit, num_fruit=num_fruit)
    )


def get_exchangerate(url='http://rate.bot.com.tw/xrt?Lang=zh-TW'):
    """
    get Taiwan bank exchange rate.
    """
    log_path = os.path.join(os.getcwd(), 'logs', log_time()+'-'+str(uuid.uuid1())+'.log')
    lazy_logger.log_to_console(logger)
    lazy_logger.log_to_rotated_file(logger=logger,file_name=log_path)
    logger.info('logger file: {0}'.format(log_path))
    
    try:
        logger.info('start connect {}'.format(url))
        resp = requests.get('http://rate.bot.com.tw/xrt?Lang=zh-TW')
        logger.info('connect success, get exchange')
        soup = BeautifulSoup(resp.text, 'html.parser')
        rows = soup.find('table', 'table').tbody.find_all('tr')
        rateset = []
        for row in rows:
            logger.info("取得: {}".format(list(row.stripped_strings)[0]))
            rateset.append(" ,".join([s for s in row.stripped_strings]))
        currency = '\n'.join(rateset)
        logger.info('get exchange success')
    except Exception as e:
        ret = OrderedDict((('ret', -1), ('status', e), ('version', '')))
        logs = get_log(file=log_path, title='get_exchangerate_job')
        ret.update(logs)
        return ret

    ret = OrderedDict((('ret', 0), ('status', 'success.'), ('values', currency), ('version', '1.00')))
    logs = get_log(file=log_path, title='get_exchangerate_job')
    ret.update(logs)
    return ret


def get_version():
    pass


def download_file():
    pass


def get_content(url):
    return requests.get(url)


def hackmd_task(url):
    """@bref open requests to parse information from hackmd.io
    """
    url = url.split('#')[0]  # get the url none anchor
    r = requests.get(url)
    if r.status_code != 200:
        return '{} error, error code; {}'.format(url, r.status_code)
    soup = BeautifulSoup(r.text, 'html.parser')
    content = soup.find(
        'div', {'id': 'doc', 'class': 'container markdown-body'})
    content = content.string

    """@bref find keywords to generate notification
    """
    if len(Archive.objects.filter(url=url)):
        compare = Archive.objects.get(url=url)
        email_subject = url
        result = Markup('<br>').join(
            diffhtml.ndiff(compare.content.splitlines(),
                           content.splitlines(), cutoff=cutoff)
        )  # default cutoff = 0.6
        diff_count = str(result).count('<ins>')
        print('上一次內容差異數: {}'.format(diff_count))
        return result
    else:
        print('第一次新增')
        Archive.objects.create(url=url, content=content)
    return 'OK, First'


if __name__ == '__main__':
    print(get_exchangerate(url='http://rate.bot.com.tw/xrt?Lang=zh-TW'))

