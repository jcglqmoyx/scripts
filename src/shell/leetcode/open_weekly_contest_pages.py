import os
from datetime import datetime


def get_interval(date1, date2):
    return abs((datetime.strptime(date1, '%Y-%m-%d') - datetime.strptime(date2, '%Y-%m-%d')).days)


if __name__ == '__main__':
    interval = get_interval('2022-10-02', datetime.now().strftime('%Y-%m-%d'))
    last = 313
    url = 'https://leetcode.com/contest/weekly-contest-%d' % (last + interval / 7)
    print(url)
    for i in range(4):
        os.system('open %s' % url)
