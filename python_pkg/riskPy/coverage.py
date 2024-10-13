# Usage python3 coverage.py cloup pandas
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
 
def get_cov_url(pack):
    url = "https://snyk.io/advisor/python/" + pack
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    d = soup.findAll('div', class_='vue--layout-container')[2].\
        findAll('img', alt=True)
    
    def get_cov_tag(x):
        if('cov' in x['src'].lower()):
            return x['src']
        else:
            return ''
    
    durl = [get_cov_tag(dd) for dd in d]
    return(''.join(durl))

def get_cov_frm_url(url):
    murl = list(url.values())[0]
    if(len(murl) > 0):
        r = requests.get(murl)
        soup = BeautifulSoup(r.content, 'html.parser')
        covr = soup.findAll('text')[-1].text
    else:
        covr = "Not Available"
    return({"Package": list(url.keys())[0],
            "Coverage(%)": covr})

if __name__ == '__main__':
    packs = sys.argv[1:]
    aurl = [{pack : get_cov_url(pack)} for pack in packs]
    cover = [get_cov_frm_url(u) for u in aurl]
    print(pd.DataFrame(cover))
