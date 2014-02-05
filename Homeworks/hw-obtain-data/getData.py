#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Jannah"
__date__ ="$Jan 31, 2014 4:21:01 PM$"
from urllib.request import urlopen
import json
import time
from pprint import pprint

def getRequest(url):
    print(url);
    response = urlopen(url);
    html = response.read().decode("utf-8");
    data = json.loads(html);
#    pprint(data);
    return html;

def writeToFile(data, file):
    f = open(file, 'w+');
#    data = data.decode('utf-8');
    f.write(data);
    
    
def merge(lsta, lstb, attr):
    for i in lstb:
        for j in lsta:
            if j[attr] == i[attr]:
                print('updating ' +j[attr]);
                j.update(i)
                break
        else:
            print('appending ' +j[attr]);
            lsta.append(i)
#    print(lsta);
    return lsta;

key = "AIzaSyCUHFlttdUG6EyjPv6FKy5y6pRfEE6HKko";
location ="37.8668,-122.2536" ;
radius = "50000";
keyword = "pizza";
type = "food";
url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+location+"&radius="+radius+"&types="+type+"&keyword="+keyword+"&sensor=false&key="+key
repeat = 1;
fileCount = 1;
nextToken = "";
allData=dict();
while repeat == 1 and fileCount<5:
    html = getRequest(url+nextToken);
    data = json.loads(html);
    
    if "next_page_token" in data:
        print("NEXT " + data["next_page_token"]);
        nextToken="&pagetoken="+data["next_page_token"];
        time.sleep(2);
        repeat=1;
    else:
        repeat=0;    

    if fileCount==1:
        allData=data;
    else:
       allData['results']= merge(allData['results'], data['results'],'id')
    fileCount = fileCount+1;

writeToFile(html, 'places.json');
#    repeat=1;
#    print (html);