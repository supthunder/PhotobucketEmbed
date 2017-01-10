# ebay avg price script
# search page for avg price and give it to you
from bs4 import BeautifulSoup
import requests
import re
import tweepy
import os
import time
from random import randint
from time import gmtime, strftime
import math
import statistics
import time 
import webbrowser


def embed(url,user,linkToAlbum):

	# change this
	mediaLink = "http://s1146.photobucket.com/"+user+"media/"
	albumsLink = "http://i1146.photobucket.com/albums/o525/"+user[5:]

	p1 = "<a href=\""+mediaLink+linkToAlbum+"/DSC_"
	p2 = "jpg.html\" target=\"_blank\"><img src=\""+albumsLink+linkToAlbum+"/DSC"
	p3 = "jpg\" border=\"0\" alt=\" photo DSC"
	p4 = "jpg\"/></a>"
	headers = {'User-agent': 'Mozilla/5.0'}
	r  = requests.get(url,headers=headers)
	data = r.text
	soup = BeautifulSoup(data,"html.parser")

	sortStr = []
	for item in soup:
		x = str(item)
		sortStr.append(x)

	parseText = sortStr[2]

	# Regex only works with DSC_1234... titles for now
	regex = re.compile('(?<=DSC).*?(?=jpg)')
	parseText = re.findall(regex,parseText)

	parseSize = set()
	count = 0
	for text in parseText:
		if len(text) == 18:
			parseSize.add(text)
	

	f = open('embed.html', 'a')
	count = 0
	for text in parseSize:
		count += 1
		print("Adding photo "+text)
		finalHtml = p1+text+p2+text+p3+text+p4
		f.write(finalHtml)
	print(count," Photos added")
	f.close()

def main():
	

	# delete old file if it exists
	try:
		os.remove('embed.html')
		print("Old file exists, deleting...")
	except OSError:
		pass

	# Change these
	user = "user/insertUserName/"
	linkToAlbum = ""


	libraryLink = "http://s1146.photobucket.com/"+user+"library/"+linkToAlbum
	url = libraryLink+"?sort=3&page="
	

	pages = int(input("Enter # of pages: ")) + 1
	for page in range(1,pages):
		url += str(page)
		print("Parsing page ",page,"...")
		embed(url,user,linkToAlbum)
		url = url[:-1]

	currentPath = os.getcwd()
	print(currentPath)
	openUrl = currentPath+"\embed.html"

	# only works with windows, use open() with mac
	webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open(openUrl)
main()
