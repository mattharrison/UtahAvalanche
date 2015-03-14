from bs4 import BeautifulSoup
import pandas as pd
import requests as r

def get_avalanches(url):
    req = r.get(url)
    data = req.text

    soup = BeautifulSoup(data)
    content = soup.find(id="content")
    trs = content.find_all('tr')
    res = []
    for tr in trs:
        tds = tr.find_all('td')
        data = {}
        for td in tds:
            name, value = get_field_name_value(td)
            if not name:
                continue
            data[name] = value
        if data:
            res.append(data)
    return res

def get_field_name_value(elem):
    tags = elem.get('class')
    start = 'views-field-field-'
    for t in tags:
        if t.startswith(start):
            return t[len(start):], ''.join(elem.stripped_strings)
        elif t == 'views-field-view-node':
            return 'url', elem.a['href']
    return None, None

def get_avalanche_detail(url, item):
    req = r.get(url + item['url'])
    data = req.text

    soup = BeautifulSoup(data)
    content = soup.find(id='content')
    field_divs = content.find_all(class_='field')
    for div in field_divs:
        key_elem = div.find(class_='field-label')
        if key_elem is None:
            print "NONE!!!", div
            continue
        key = ''.join(key_elem.stripped_strings)
        try:
            value_elem = div.find(class_='field-item')
            value = ''.join(value_elem.stripped_strings).\
                    replace(u'\xa0', u' ')
        except AttributeError as e:
            print e, div
        if key in item:
            continue
        item[key] = value
    return item

def get_avalanche_details(url):
    res = []
    for item in rows:
        item = get_avalanche_detail(url, item)
        res.append(item)
    return res


def crawl(outname, size=10):
    base = 'https://utahavalanchecenter.org/'
    url = base + 'avalanches/fatalities'
    items = get_avalanches(url)
    details = get_avalanche_details(base, items[:size])
    #return details
    df = pd.DataFrame(details)
    df.to_csv(outname, encoding='utf-8')


if __name__ == '__main__':
    crawl('/tmp/ava-all.csv', 100)
