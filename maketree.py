#! /usr/bin/env python2

import sys

from graphviz import Digraph
import requests
import bs4
from bs4 import BeautifulSoup as bs

import json


tree = {}
to_process = []

def parseLevel(currentLevel, url):

    #original = requests.get('http://www.familyorigins.com/users/b/u/c/Gordon-S-Buck/FAMO1-0001/d244.htm#P244')
    original = requests.get(url)

    page = bs(original.text)

    for image in page.find_all('img'):
        alt = image.get('alt')
        if alt == 'child':
            child = image.find_next_sibling('b')
            for element in child.contents:
                if isinstance(element, bs4.element.Tag):
                    if element.contents:
                        currentLevel[element.contents[0]] = {}
                        if element.get('href'):
                            print 'Will process %s' % element.contents[0]
                            to_process.append((currentLevel[element.contents[0]], 'http://www.familyorigins.com/users/b/u/c/Gordon-S-Buck/FAMO1-0001/' + element.get('href')))
                else:
                    if element:
                        print 'Will not process %s' % element.strip()
                        currentLevel[element.strip()] = None

tree['Thomas BUCK I'] = {}
to_process.append((tree['Thomas BUCK I'], 'http://www.familyorigins.com/users/b/u/c/Gordon-S-Buck/FAMO1-0001/d255.htm#P253'))

while to_process:
    parseLevel(*to_process[0])
    to_process = to_process[1:]

json.dumps(tree)
