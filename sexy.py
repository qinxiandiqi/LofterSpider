#!/usr/bin/python
# -*- coding:utf8 -*-

from bs4 import BeautifulSoup

import urllib2,re,os

currentPath = os.getcwd()
imagePath = os.path.join(currentPath, u'images')
if not os.path.isdir(imagePath):
	os.mkdir(imagePath)

ALL_DOWNLOADS = 0

def scrapyImages(page=1):
	global ALL_DOWNLOADS
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
			groupID = descriptMeta["content"].split(" ")[0]
		print groupID
		targetDirPath = os.path.join(imagePath, groupID)
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
		print u"\nStart next page..."
		scrapyImages(page)
	else:
		print u"Prograss Done!"
		print u"All download %s images" % ALL_DOWNLOADS

scrapyImages()

raw_imput("Press <Enter> To Quit!")
