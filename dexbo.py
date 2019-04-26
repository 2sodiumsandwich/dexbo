#!/usr/bin/python3
from scraper import getpokelink, pokescraper

t = getpokelink(input("Search query: "))
if(t): print(pokescraper(t))