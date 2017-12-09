#!/usr/bin/python
# -*- coding:utf8 -*-

from bs4 import BeautifulSoup

import urllib2,re,os,argparse,thread,time,hashlib,traceback

ALL_DOWNLOADS = 0
START_PAGE = 1
END_PAGE = 65589
BASE_DIR = u"images"
IMAGE_DIR_PATH = ''
DOMAIN_DIR_PATH = ''
KEEP_WORKING = True
MAX_PAGE_ERROR_TIMES = 3
CURRENT_PAGE_ERROR_TIMES = 0
ONLY_LATEST_IMAGES = False
DOMAIN = u"mybluecat"
IS_GROUP_BY_DATE = True
TIME_OUT = 60

def initArgs():
	global START_PAGE,END_PAGE,BASE_DIR,MAX_PAGE_ERROR_TIMES,ONLY_LATEST_IMAGES,DOMAIN,IS_GROUP_BY_DATE,TIME_OUT
	parse = argparse.ArgumentParser()
	parse.add_argument('-s', '--startpage', dest='startpage', type=int, nargs='?', const=1, default=1, help='The first page to scrapy, default is 0.')
	parse.add_argument('-e', '--endpage', dest='endpage', type=int, nargs='?', const=65589, default=65589, help='The last page to scrapy, default is 65589.')
	parse.add_argument('-d', '--dir', dest='basedir', type=str, nargs='?', const=u"images", default=u"images", help='The base dir to save image, default is images')
	parse.add_argument('-m', '--max', dest='maxtimes', type=int, nargs='?', const=3, default=3, help='The max times to try next page when the current page get fail, default is 3')
	parse.add_argument('-n', '--new', dest='getnew', action='store_true', default=False, help='Set only to get the latest images.')
	parse.add_argument('--domain', dest='domain', type=str, nargs='?', const=u"mybluecat", default=u"mybluecat", help='The secondary domain of target lofter page, default is mybluecat')
	parse.add_argument('--groupByDate', dest='groupByDate', action='store_false', default=True, help='Group image with its publish date, default is true')
	parse.add_argument('-t', '--timeout', dest='timeout', type=int, nargs='?', const=60, default=60, help='The timeout of a http connection, default is 60')
	args = parse.parse_args()
	ONLY_LATEST_IMAGES = args.getnew
	if ONLY_LATEST_IMAGES:
		START_PAGE = 1
	else:
		START_PAGE = args.startpage
	END_PAGE = args.endpage
	BASE_DIR = args.basedir
	MAX_PAGE_ERROR_TIMES = args.maxtimes
	DOMAIN = args.domain
	IS_GROUP_BY_DATE = args.groupByDate
	TIME_OUT = args.timeout
	print u"\n======================================================================"
	print u"Progress Setting:"
	print u"1.Search from %s page to %s page." % (START_PAGE, END_PAGE)
	print u"2.Save images to %s dir" % BASE_DIR
	print u"3.Max type next page time is %s." % MAX_PAGE_ERROR_TIMES
	print u"4.Only get the latest images? %s" % ONLY_LATEST_IMAGES
	print u"5.The target domain is %s" % DOMAIN
	print u"6.Is group image by publish date? %s" % IS_GROUP_BY_DATE

def initBasePath():
	global BASE_DIR,IMAGE_DIR_PATH,DOMAIN_DIR_PATH
	currentPath = os.getcwd()
	IMAGE_DIR_PATH = os.path.join(currentPath, BASE_DIR)
	if not os.path.isdir(IMAGE_DIR_PATH):
		os.mkdir(IMAGE_DIR_PATH)
	DOMAIN_DIR_PATH = os.path.join(IMAGE_DIR_PATH, DOMAIN)
	if not os.path.isdir(DOMAIN_DIR_PATH):
		os.mkdir(DOMAIN_DIR_PATH)

def inputHandle():
	global KEEP_WORKING
	print u"Now start scrapy progress,you can type ENTER key to stop anytime..."
	print u"=======================================================================\n"
	raw_input()
	KEEP_WORKING = False
	print "Handle the working progress, please wait...\n"
	
def scrapyImages(page=1):
	global ALL_DOWNLOADS,START_PAGE,END_PAGE,BASE_DIR,DOMAIN_DIR_PATH,KEEP_WORKING,MAX_PAGE_ERROR_TIMES,CURRENT_PAGE_ERROR_TIMES,ONLY_LATEST_IMAGES,IS_GROUP_BY_DATE,TIME_OUT
	KEEP_WORKING = True
	thread.start_new(inputHandle,())
	time.sleep(1)
	while KEEP_WORKING:
		pageUrl = r"http://%s.lofter.com/?page=%s" % (DOMAIN, page)
		print pageUrl
		try:
			pageContent = urllib2.urlopen(pageUrl, timeout=TIME_OUT)
			CURRENT_PAGE_ERROR_TIMES = 0
		except:
			CURRENT_PAGE_ERROR_TIMES = CURRENT_PAGE_ERROR_TIMES + 1
			if CURRENT_PAGE_ERROR_TIMES >= MAX_PAGE_ERROR_TIMES:
				print u"Get %s pages failed,please check your network or try later" % MAX_PAGE_ERROR_TIMES
				break
			else:
				print u"Get %s page failed, try next page...\n" % page
				continue
		pageSoup = BeautifulSoup(pageContent)
		imageGroup = pageSoup.find_all("a", class_="img", href=re.compile("post"))
		imageGroupCount = 0
		for groupItem in imageGroup:
			if not KEEP_WORKING:
				break
			groupUrl = groupItem.get("href")
			print groupUrl
			imageGroupCount = imageGroupCount + 1
			try:
				groupContent = urllib2.urlopen(groupUrl, timeout=TIME_OUT)
				groupSoup = BeautifulSoup(groupContent)
				groupID = u"default"
				if IS_GROUP_BY_DATE:
					dateTag = groupSoup.find("a", class_="date")
					if dateTag is not None:
						groupID = dateTag.string
						if groupID is None:
							groupID = u"default"
							print u"Get publish date for groupID fail, set to default"
						if len(groupID) == 0 or len(groupID) > 12:
							print groupID + "-" + str(len(groupID))
							groupID = u"default"
				print u"GroupID is " + groupID
			except Exception, e:
				print u"Get this group images fail, try next gourp..."
				print traceback.format_exc()
				continue
			targetDirPath = os.path.join(DOMAIN_DIR_PATH, groupID)
			if not os.path.isdir(targetDirPath):
				os.mkdir(targetDirPath)
			images = groupSoup.find_all("div", class_="pic")
			for imageItem in images:
				if not KEEP_WORKING:
					break
				imageUrl = imageItem.a.img.get("src")
				try:
					imageContent = urllib2.urlopen(imageUrl, timeout=TIME_OUT).read()
				except:
					print "Get image fail:" + imageUrl
					continue
				try:
					imageSavePath = targetDirPath + "/" + imageUrl.split("/")[-1].split("?")[0]
				except:
					print u"Get image name fail, set a md5 name"
					imageSavePath = targetDirPath + "/" + hashlib.md5(imageUrl).hexdigest()
				if os.path.exists(imageSavePath):
					if ONLY_LATEST_IMAGES:
						print "Have got all latest images"
						KEEP_WORKING = False
						break
					print "Image is existed:" + imageSavePath
					continue
				try:
					with open(imageSavePath, 'wb') as datas:
						datas.write(imageContent)
				except:
					print "Save image fail:" + imageSavePath
					continue
				ALL_DOWNLOADS = ALL_DOWNLOADS + 1
				print "Save image success:" + imageSavePath
		print u"Parse %s page  %s image groups. " % (page,imageGroupCount)
		if imageGroupCount > 0 and KEEP_WORKING:
			page = int(page) + 1
			if int(page) > END_PAGE:
				KEEP_WORKING = False
			else:
				print u"-------------------------------------------"
				print u"Start next page..."
		else:
			KEEP_WORKING = False
	else:
		print u"======================================"
		print u"Progress Done!"
		print u"All download %s images" % ALL_DOWNLOADS
		print u"======================================"

initArgs()
initBasePath()
try:
	scrapyImages(START_PAGE)
except KeyboardInterrupt:
	print "Unnatural exit.\nIf you want to cancel the progress,please type ENTER key."
except:
	print "Unkown exception."
	
