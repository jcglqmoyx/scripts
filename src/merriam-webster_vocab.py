import requests  
from bs4 import BeautifulSoup  
  
headers = {  
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '  
                  'AppleWebKit/537.36 (KHTML, like Gecko) '                  'Chrome/91.0.4472.114 Safari/537.36',  
}  
base_url = 'https://www.merriam-webster.com/browse/dictionary/'  
  
  
def get_words(url: str) -> None:  
    print('extracting words from page %s' % url)  
    try:  
        file = open('word.txt', 'a')  
        res = requests.get(url, headers=headers)  
        html_data = str(res.content, 'utf-8')  
        soup = BeautifulSoup(html_data, 'lxml')  
        words = soup.select('div.mw-grid-table-list ul li a span')  
        for word in words:  
            file.write(word.text)  
            file.write('\n')  
        file.close()  
    except Exception as e:  
        print(e)  
        print('retrying parsing page %s' % url)  
        get_words(url)  
  
  
def main():  
    categories = []  
    for c in range(ord('a'), ord('z') + 1):  
        categories.append(chr(c))  
  
    for uri in categories:  
        url = base_url + uri  
        html = requests.get(url, headers=headers).content  
        html_data = str(html, 'utf-8')  
        soup = BeautifulSoup(html_data, 'lxml')  
        cnt_page = len(soup.select(  
            'div.outer-container div.main-container div div div.left-content div.browse-letter div ul li div span'))  
        print(url)  
        print(cnt_page)  
        for i in range(1, cnt_page + 1):  
            get_words(url + '/' + str(i))  
  
  
if __name__ == '__main__':  
    main()
