from bs4 import BeautifulSoup
import requests
import re
import os
import webbrowser


def embed(url,user,linkToAlbum):

	# change this
	mediaLink = "http://s1146.photobucket.com/"+user+"media/"
	albumsLink = "http://i1146.photobucket.com/albums/o525/"+user[5:]

	p1 = "<a href=\""+mediaLink+linkToAlbum+"/DSC"
	p2 = "jpg.html\" target=\"_blank\"><img class=\"mySlides\" img src=\""+albumsLink+linkToAlbum+"/DSC"
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

	f = open('embed.html', 'a')
	styleSheet = "<link rel=\"stylesheet\" href=\"http://www.w3schools.com/lib/w3.css\">"
	styleSheet += "<div class=\"w3-content w3-display-container\">"
	f.write(styleSheet)
	f.close()

	user = "user/"
	# Change username
	user += "userName"

	user += "/"

	# Change the link to album
	# For example:
	linkToAlbum = "Some%20Name%201%20%20Name%20-%20name"


	libraryLink = "http://s1146.photobucket.com/"+user+"library/"+linkToAlbum
	url = libraryLink+"?sort=3&page="


	pages = int(input("Enter # of pages: ")) + 1
	for page in range(1,pages):
		url += str(page)
		print("Parsing page ",page,"...")
		embed(url,user,linkToAlbum)
		url = url[:-1]

	f = open('embed.html', 'a')
	jsScript = "<a class=\"w3-btn-floating w3-display-left\" onclick=\"plusDivs(-1)\">&#10094;</a>"
	jsScript += "<a class=\"w3-btn-floating w3-display-right\" onclick=\"plusDivs(1)\">&#10095;</a></div>"
	jsScript += "<script> var slideIndex = 1; showDivs(slideIndex); function plusDivs(n) { showDivs(slideIndex += n);"
	jsScript += " } function showDivs(n) { var i; var x = document.getElementsByClassName(\"mySlides\");"
	jsScript += " if (n > x.length) {slideIndex = 1} if (n < 1) {slideIndex = x.length}"
	jsScript += " for (i = 0; i < x.length; i++) { x[i].style.display = \"none\"; }"
	jsScript += " x[slideIndex-1].style.display = \"block\"; } </script>"
	f.write(jsScript)
	f.close()

	currentPath = os.getcwd()
	print(currentPath)

	# Windows only
	openUrl = currentPath+"\embed.html"
	webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open(openUrl)
main()
