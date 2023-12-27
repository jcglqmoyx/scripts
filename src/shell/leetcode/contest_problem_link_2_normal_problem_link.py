import os

link = input('link: ')
i, j = link.index('contest'), link.index('problems')
link = link[:i] + link[j:]
os.system('open %s' % link)

