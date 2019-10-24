from urllib.request import urlopen, urljoin, Request
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://www.youtube.com"
default_url = "https://www.youtube.com/channel/UCFdTiwvDjyc62DBWrlYDtlQ/search?query=scrapy"

page = urlopen(default_url).read()
soup = BeautifulSoup(page, features='lxml')
suburl = soup.select('a[href*="/watch?"]')

v_url = []
for i in suburl:
    #print(urljoin(base_url, i['href']))
    v_url.append(urljoin(base_url, i['href']))

v_url = list(set(v_url))
d_frame = pd.DataFrame(columns=['Date', 'Title', 'URL'])
print(d_frame)

for i in v_url:
    v_page = urlopen(i)
    v_soup = BeautifulSoup(v_page,features='lxml')

    #v_title = v_soup.title.get_text().split(' - YouTube')[0]
    #print(v_title, '\t', i)
    v_title, v_date = '', ''
    try:
        v_title = v_soup.title.get_text().split(' - YouTube')[0]
        v_date = v_soup.find('meta', {'itemprop': 'uploadDate'})['content']
    except Exception as e:
        pass
    
    new = pd.DataFrame( { 'Date': v_date, 'Title': v_title, 'URL': i }, index=[0] )
    #print(new)
    d_frame = d_frame.append(new, ignore_index=True)

#print(d_frame.sort_values(by=['Date'], index=False))
d_frame.sort_values(by=['Date']).to_csv('Result.csv', columns=['Date', 'Title', 'URL'], index=False)