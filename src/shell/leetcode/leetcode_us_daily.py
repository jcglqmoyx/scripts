import os
import time

if __name__ == '__main__':
    link = input('> ')
    apps = ['Google Chrome', 'Safari', 'Firefox', 'Google Chrome Canary', 'Microsoft Edge', 'Vivaldi', 'Brave Browser']
    for app in apps:
        os.system(f'open -a "{app}" %s' % link)
        time.sleep(1)
