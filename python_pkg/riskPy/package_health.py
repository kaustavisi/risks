import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

class Score:
    def __init__(self, package):
        self.Package = package
        self.Score = None
        self.DownloadLastMonth = None
        self.Popularity = None
        self.Maintenance = None
        self.Security = None
        self.Community = None
        self.LastRelease = None
        self.Age = None
        self.LastCommit = None
        self.Readme = None
        self.Maintainers = None
        self.GitHubStars = None
        self.Versions = None
        
    def get_download_stat(self):
        url = "https://pypistats.org/packages/" + self.Package
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        a = soup.findAll('p')
        x = []
        for br in a[1].findAll('br'):
            next_s = br.nextSibling
            x.append(next_s)
        down = [w.replace('\n', '').replace(',', '').\
            split(':')[1] for w in x[-3:]]
        self.DownloadLastMonth = down[2]

    def get_package_health(self):
        url = "https://snyk.io/advisor/python/" + self.Package
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        ## Get Security, Popularity, Maintenance & Community stats 
        d = soup.findAll('div', class_='package-extra')[0].\
            findAll('div', class_='health')[0].\
            findAll('div', class_='vue--pill--uppercase')
        self.Score = soup.findAll('title')[2].text.split(":")[1]
        self.Security = d[0].text
        self.Popularity = d[1].text
        self.Maintenance = d[2].text
        self.Community = d[3].text
        dd = [x.text.split('\n')[:2] for x in soup.findAll('div', class_='stats-item')]
        df = {}
        for x in dd:
            df[x[0].strip()] = x[1].strip()
        self.GitHubStars = df['GitHub Stars']
        self.LastCommit = df['Last Commit']
        self.LastRelease = df['Last Release']
        self.Versions = df['Versions']
        self.Maintainers = df['Maintainers']
        self.Age = df['Age']
        self.Readme = df['Readme']
    

    def risk_summary(self):
        return(pd.DataFrame({
            'Package': self.Package, 
            'Score': self.Score,
            'Download (Last Month)': self.DownloadLastMonth,
            'Popularity': self.Popularity,
            'Maintenance': self.Maintenance,
            'Security': self.Security,
            'Age': self.Age,
            'Community': self.Community,
            'Last Release': self.LastRelease,
            'Last Commit': self.LastCommit,
            'Readme': self.Readme,
            'Maintainers': self.Maintainers,
            'GitHubStars': self.GitHubStars,
            'Versions': [self.Versions]
        }))

    def print_risk(self):
        rs = self.risk_summary()
        for col in rs.columns:
            print(f'{col} : {rs.iloc[0][col]}')

def calc_score(pack):
    print(f'Calculating risk of {pack}...')

    p1 = Score(package = pack)
    p1.get_download_stat()
    p1.get_package_health()
    print('---------------------------------------------')
    p1.print_risk()
    print('---------------------------------------------')

if __name__ == '__main__':
    for pack in sys.argv[1:]:
        calc_score(pack)


