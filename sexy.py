#!/usr/bin/python
# -*- coding:utf8 -*-

from bs4 import BeautifulSoup

import urllib2,re,os,argparse

ALL_DOWNLOADS = 0
START_PAGE = 0
END_PAGE = 65589
BASE_DIR = u"images"
IMAGE_DIR_PATH = ''

def initArgs():
	global START_PAGE,END_PAGE,BASE_DIR
	parse = argparse.ArgumentParser()
	parse.add_argument('-s', '--startpage', dest='startpage', type=int, nargs='?', const=0, default=0, help='The first page to scrapy, default is 0.')
	parse.add_argument('-e', '--endpage', dest='endpage', type=int, nargs='?', const=65589, default=65589, help='The last page to scrapy, default is 65589.')
	parse.add_argument('-d', '--dir', dest='basedir', type=str, nargs='?', const=u"images", default=u"images", help='The base dir to save image, default is images')
	args = parse.parse_args()
	START_PAGE = args.startpage
	END_PAGE = args.endpage
	BASE_DIR = args.basedir
	print u"Save image to %s and Search from %s page to %s page..." % (BASE_DIR, START_PAGE, END_PAGE)	

def initBasePath():
	global BASE_DIR,IMAGE_DIR_PATH
	currentPath = os.getcwd()
	IMAGE_PATH = os.path.join(currentPath, BASE_PATH)
	if not os.path.isdir(IMAGE_DIR_PATH):
		os.mkdir(IMAGE_DIR_PATH)

def scrapyImages(page=1):
	global ALL_DOWNLOADS,START_PAGE,END_PAGE,BASE_PATH,IMAGE_DIR_PATH
	pageUrl = r"http://me2-sex.lofter.com/?page=%s" % page
	print pageUrl
	pageContent = urllib2.urlopen(pageUrl)
	pageSoup = BeautifulSoup(pageContent)
	imageGroup = pageSoup.find_all("a", class_="img", href=re.compile("post"))
	imageGroupCount = 0
	for groupItem in imageGroup:
		groupUrl = groupItem.get("href")
		print groupUrl
		imageGroupCount = imageGroupCount + 1
		groupContent = urllib2.urlopen(groupUrl)
		groupSoup = BeautifulSoup(groupContent)
		groupID = u"default"
		descriptMeta = groupSoup.find("meta", attrs={"name": "Description"})
		if descriptMeta is  None:
			groupID = u"default"
		else:
			groupID = descriptMeta["content"].strip()
			if len(groupID) == 0:
				groupID = u"default"
			else:
				groupID = groupID.split(" ")[0]
		print groupID
		targetDirPath = os.path.join(IMAGE_DIR_PATH, groupID)
		if not os.path.isdir(targetDirPath):
			os.mkdir(targetDirPath)
		images = groupSoup.find_all("div", class_="pic")
		for imageItem in images:
			imageUrl = imageItem.a.img.get("src")
			imageContent = urllib2.urlopen(imageUrl).read()
			imageSavePath = targetDirPath + "/" + imageUrl.split("/")[-1]
			if os.path.exists(imageSavePath):
				print "Image is exist:" + imageSavePath
				continue
			with open(imageSavePath, 'wb') as datas:
				datas.write(imageContent)
			ALL_DOWNLOADS = ALL_DOWNLOADS + 1
			print imageUrl
	print u"This page has %s image groups. " % imageGroupCount
	if imageGroupCount > 0:
		page = int(page) + 1
		if int(page) > END_PAGE:
			print u"Prograss Done!"
			print u"All download %s images" % ALL_DOWNLOADS
		else:
			print u"\nStart next page..."
			scrapyImages(page)
	else:
		print u"Prograss Done!"
		print u"All download %s images" % ALL_DOWNLOADS

initArgs()
scrapyImages(START_PAGE)

raw_input("Press <Enter> To Quit!")
