#!/usr/bin/env python
import urllib2
from bs4 import BeautifulSoup
import re
import json
import pdb
import time
import pytz
import datetime
import httplib
import socket
from calendar import timegm
import xml.etree.ElementTree as ET
from itertools import islice

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

met = pytz.timezone("Europe/Berlin")


urlDEPs = "https://www.vgn.de/abfahrten/?dm=de%3A09574%3A7000&excl=Bus,Demandbus"

source = urllib2.urlopen(urlDEPs).read()
soup = BeautifulSoup(source, "lxml", from_encoding='utf8')
soup.prettify


def get_connections():
    connections = []
    conn = {}

    for c in soup.findAll('tr', { 'class': re.compile('classS_Bahn')}):
        conn['platform'] = c.find('span', { 'class': "EFA-Gleis"}).get_text()
        conn['destination'] = c.find('span', { 'class': "EFA-Richtung"}).get_text()
        conn['line'] = c.find('a', { 'class': "EFA-Linienlink" }).get_text()
        conn['departure'] = c.find('span', { 'class': "EFA-TimeDetail" }).get_text()
        conn['delay'] = c.find('span', { 'class': re.compile('delay-*')}).get_text() or "+0"
        connections.append(conn.copy())
        #pdb.set_trace()
    print(json.dumps(connections,ensure_ascii=False).encode("utf8"))
    return json.dumps(connections,ensure_ascii=False).encode("utf8")

def update():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 4444))
    s.recv(1000)
    s.send("departures\n")
    s.recv(1000)
    departures = get_connections()
    s.send(departures)
    s.send("\n")
    s.close()

def send_clock():
    now, timestamp = current_time()
    udp.sendto('departures/clock/set:%f' % timestamp, ('127.0.0.1', 4444))

def current_time():
    now = datetime.datetime.utcnow()
    timestamp = timegm(now.timetuple()) + now.microsecond / 1000000.
    now = now.replace(tzinfo=pytz.utc)
    now = now.astimezone(met)
    now = now.replace(tzinfo=None)
    return now, timestamp

def main():
    time.sleep(5)
    send_clock()
    while 1:
        update()
        for i in xrange(6):
            time.sleep(10)
            send_clock()

if __name__ == "__main__":
    main()

# with open('data.log', 'w') as outfile:
#     json.dump(connections, outfile)



#    print("%s %s\t%s\t%s\t%s" % (dep,delay,line,platform,dest))
