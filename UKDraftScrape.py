from bs4 import BeautifulSoup
import csv
import requests
from time import sleep

Schoolname = ["Kentucky"]


BASE_URL = "http://www.nbadraft.net/nba_draft_history/index.html"
STEM_URL = "http://www.nbadraft.net"

def makesoup(url):
    return BeautifulSoup(requests.get(url).text)

soup = makesoup(BASE_URL)
divyclass = soup.find("div", {"class":"node-inner"}).tbody

links = [STEM_URL + row.a["href"] for row in divyclass.findAll("td") if row.a and int(row.a.text.split("-")[0])>=2010]

wildcatlist = []
draftpicknumberlist = []

#for the historical draft results
for link in links:
    soup2 = makesoup(link)
    for row in soup2.find("div", {"id":"content-area"}).tbody('tr'):
        tds = row('td')
        for eachschool in Schoolname:
            if eachschool in tds[6].string:
                wildcatlist.append(STEM_URL + tds[2].a["href"])
                draftpicknumberlist.append(int(tds[0].string))
            if eachschool in tds[14].string:
                wildcatlist.append(STEM_URL + tds[10].a["href"])
                draftpicknumberlist.append(int(tds[8].string))

#for the 2015 mock draft
soup3 = makesoup('http://www.nbadraft.net/2015mock_draft')           
navigatesoup = soup3.findAll("div", {"id":"content-area"})[0].findAll('tbody')[1]('tr')
for row in navigatesoup:
    tds = row('td')
    for eachschool in Schoolname:
        if eachschool in tds[6].string:
            wildcatlist.append(STEM_URL + tds[2].a["href"])
        
print wildcatlist   
print len(wildcatlist)

with open("UKDraftScouting.csv", "w") as f:
    headers = ["Report"]
    writer = csv.writer(f, delimiter = ",")
    writer.writerow(headers)

    for wildcat in wildcatlist:
        wildsoup = makesoup(wildcat)
        report = wildsoup.find("div", {"id":"nbap_content_bottom"}).find('p').text.encode("utf-8")
        
        sleep(0.5)
        writer.writerow([report])
print 'Done'