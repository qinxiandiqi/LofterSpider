#!/usr/bin/python
# -*- coding:utf8 -*-

import urllib2
import re
import os
import argparse
import thread
import time
import pickle
import signal
import sys

from bs4 import BeautifulSoup


all_downloads = 0
base_dir = u"atlas_images"
setting_dir = u'setting'
keep_working = True
max_page_error_times = 3
currrent_page_error_times = 0
download_from_last_id = False
target_name = ''
target_id = ''
view_cache = False

main_domain = r'http://girl-atlas.com/'
tag_domain = main_domain + r'tag.action?id=%s&last='
index_domain = main_domain + r"index.action?id=2&last="
search_tag_url = main_domain + r"searchTag.action?word="
target_url = index_domain

header = r'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'

group_dice = {}
girl_dice = {}
lastid_dice = {}
group_cache_file = u'group_dice'
girl_cache_file = u'girl_dice'
lastid_cache_file = u"last_id"

def init_env():
	reload(sys)
	sys.setdefaultencoding('utf-8')

def init_args():
	global base_dir, max_page_error_times, download_from_last_id, target_id, target_name, view_cache
	parse = argparse.ArgumentParser()
	parse.add_argument('-d', '--dir', dest='basedir', type=str,
		nargs='?', const=u"images", default=u"atlas_images",
		help='The base dir to save image, default is images')
	parse.add_argument('-m', '--max', dest='maxtimes', type=int,
		nargs='?', const=3, default=3,
		help='The max times to try next page when the current page get fail, default is 3')
	parse.add_argument('-t', '--tag', dest='tag', type=str,
		nargs='?', const=None, default=None,
		help=u"The target tag name, default will not used.")
	parse.add_argument('-i', '--id', dest='tag_id', type=str,
		nargs='?', const=None, default=None,
		help=u"The target tag id, default will not used.")
	parse.add_argument('-l', '--last', dest='last', action='store_true', default=False,
		help=u"Download from the last download, default is false.")
	parse.add_argument('-v', '--view', dest='view_cache', action='store_true', default=False,
		help=u"View the cache tag.")
	args = parse.parse_args()
	base_dir = args.basedir
	max_page_error_times = args.maxtimes
	target_name = args.tag
	target_id = args.tag_id
	download_from_last_id = args.last
	view_cache = args.view_cache
	print(u"\n======================================================================")
	print(u"Progress Setting:")
	print(u"1.Save images to %s dir" % base_dir)
	print(u"2.Max type next page time is %s." % max_page_error_times)
	print(u"Note:you can use Ctrl+C or Ctrl+Z to cancel progress")
	print(u"======================================================================\n")

def init_dir_and_file():
	global base_dir, setting_dir, group_cache_file, girl_cache_file, lastid_cache_file
	current_path = os.getcwd()
	base_dir = os.path.join(current_path, base_dir)
	if not os.path.isdir(base_dir):
		os.mkdir(base_dir)
	setting_dir = os.path.join(current_path, setting_dir)
	if not os.path.isdir(setting_dir):
		os.mkdir(setting_dir)
	group_cache_file = setting_dir + "/" + group_cache_file
	girl_cache_file = setting_dir + "/" + girl_cache_file
	lastid_cache_file = setting_dir + "/" + lastid_cache_file
	print(group_cache_file)
	print(girl_cache_file)
	print(lastid_cache_file)

def init_dice():
	global group_dice, girl_dice,lastid_dice, group_cache_file, girl_cache_file, lastid_cache_file
	try:
		with open(group_cache_file, 'r') as group_file:
			group_dice = pickle.load(group_file)
	except:
		print(u"Get group dice cache file fail, using null dice.")
		group_dice = {}
	try:
		with open(girl_cache_file, 'r') as girl_file:
			girl_dice = pickle.load(girl_file)
	except:
		print(u"Get girl dice cache file fail, using null dice.")
		girl_dice = {}
	try:
		with open(lastid_cache_file, 'r') as lastid_file:
			lastid_dice = pickle.load(lastid_file)
	except:
		print(u"Get lastid dice cache file fail, using null dice.")
		lastid_dice = {}

def save_dice():
	global group_dice, girl_dice, lastid_dice, group_cache_file, girl_cache_file, lastid_cache_file
	try:
		with open(group_cache_file, 'w') as group_file:
			pickle.dump(group_dice, group_file)
	except:
		print(u"Sorry, save group name data fail.")
	try:
		with open(girl_cache_file, 'w') as girl_file:
			pickle.dump(girl_dice, girl_file)
	except:
		print(u"Sorry, save girl name data fail.")
	try:
		with open(lastid_cache_file, 'w') as lastid_file:
			pickle.dump(lastid_dice, lastid_file)
	except:
		print(u"Sorry, save lastid data fail.")
	print(u"Save dice data done!")

def search_tag_id_by_name(name):
	global group_dice, girl_dice, search_tag_url
	if group_dice.has_key(name):
		return group_dice.get(name, None)
	elif girl_dice.has_key(name):
		return girl_dice.get(name, None)
	else:
		try:
			search_content = urllib2.urlopen(search_tag_url + name)
		except:
			return None
		search_soup = BeautifulSoup(search_content)
		li_tag = search_soup.find(tid=True)
		if li_tag is None:
			return None
		else:
			return li_tag.get('tid')

def get_target_url():
	global index_domain, tag_domain, target_url, target_name, target_id
	if target_name is None and target_id is None:
		target_url = index_domain
		target_id = u"index"
	elif target_id is not None:
		target_url = tag_domain % target_id
	else:
		target_id = search_tag_id_by_name(target_name)
		if target_id is None:
			print(u"Sorry, can't found %s tag" % target_name)
			return None
		else:
			target_url = tag_domain % target_id
	return target_url

def add_cache_last_id_for_url(url):
	global download_from_last_id, lastid_dice, target_id
	if download_from_last_id and (target_id is not None) and lastid_dice.has_key(target_id):
		url = url + lastid_dice.get(target_id, '')
	return url

def list_tag():
	global group_dice,girl_dice
	index = 0
	row = ""
	print(u"The group tag:")
	for key in group_dice:
		row = row + key + ":" + group_dice.get(key, None) + "\t\t"
		index = index + 1
		if index == 3:
			print(row)
			index = 0
			row = ''
	if index < 3 and index > 0:
		print(row)
	index = 0
	row = ''
	print(u"The girl tag:")
	for key in girl_dice:
		row = row + key + ":" + girl_dice.get(key, None) + '\t\t'
		index = index + 1
		if index == 3:
			print(row)
			index = 0
			row = ''
	if index < 3 and index > 0:
		print(row)

def signal_handler(signum, frame):
	global keep_working
	keep_working = False
	print(u"\nStart finish the last progress and will auto exit...")
	print(u"(If there is any questions,please answer first)")
	
def scrapy_images():
	global all_downloads, base_dir, keep_working, max_page_error_times, current_page_error_times, group_dice, girl_dice, lastid_dice, target_id, target_url, header
	keep_working = True 
	target_url = get_target_url()
	if target_url is None:
		return
	page_url = add_cache_last_id_for_url(target_url)
	while keep_working:
		print(page_url)
		try:
			page_content = urllib2.urlopen(page_url)
			current_page_error_times = 0
		except:
			current_page_error_times = current_page_error_times + 1
			if current_page_error_times >= max_page_error_times:
				print(u"Get page failed %s times,please check your network and try later" % max_page_error_times)
				break
			else:
				print(u"Get page failed, try again...\n")
				continue
		page_soup = BeautifulSoup(page_content)
		image_group = page_soup.find_all("div", class_="grid_title")
		image_group_count = 0
		for group_item in image_group:
			if not keep_working:
				break
			group_url = group_item.a.get("href")
			print(group_url)
			image_group_count = image_group_count + 1
			try:
				group_content = urllib2.urlopen(group_url)
			except:
				print(u"Get this group images fail, try next gourp...")
				continue
			group_soup = BeautifulSoup(group_content)
			atlas_id = u"default"
			tags = group_soup.find("div", class_="album_tags").find_all('a')
			for i in range(len(tags)):
				tag_name = tags[i].string
				if tag_name is None:
					print tags[i]
					continue
				tag_name = tag_name.strip()
				if girl_dice.has_key(tag_name):
					atlas_id = tag_name
					break
				elif group_dice.has_key(tag_name):
					if i == 0:
						atlas_id = tag_name
				else:
					tag_code = tags[i].get('href').split('/')[-1].strip()
					your_choose = raw_input(tag_name + u" is a girl's name?(y/n):")
					if your_choose.strip().lower() == 'y':
						girl_dice.setdefault(tag_name, tag_code)
						atlas_id = tag_name
						break
					else:
						group_dice.setdefault(tag_name, tag_code)
						if i == 0:
							atlas_id = tag_name
			print(atlas_id)
			#continue	
			target_dir_path = os.path.join(base_dir, atlas_id)
			if not os.path.isdir(target_dir_path):
				os.mkdir(target_dir_path)
			images = group_soup.find_all("li", class_="slide")
			for image_item in images:
				if not keep_working:
					break
				image_url = image_item.img.get("src")
				if image_url is None:
					image_url = image_item.img.get("delay")
				try:
					req = urllib2.Request(image_url)
					req.add_header('User-Agent', header)
					image_content = urllib2.urlopen(req).read()
				except:
					print(u"get image fail:" + image_url)
					continue
				image_save_path = target_dir_path + "/" + image_url.split("/")[-1].split("!")[0]
				if os.path.exists(image_save_path):
					print(u"Image is existed:" + image_save_path)
					continue
				try:
					with open(image_save_path, 'wb') as datas:
						datas.write(image_content)
				except:
					print(u"Save image fail:" + image_save_path)
					continue
				all_downloads = all_downloads + 1
				print(u"Save image success:" + image_save_path)
			lastid_dice.setdefault(target_id, group_url.split('/')[-1])
		print u"Parse this page  %s image groups. " % image_group_count
		last_group_id = image_group[-1].a.get('href').split('/')[-1]
		if (not keep_working) or (last_group_id is None) or (image_group_count == 0):
			keep_working = False
		else:
			page_url = target_url + last_group_id
			keep_working = True
	else:
		print(u"======================================")
		print(u"Progress Done!")
		print(u"All download %s images" % all_downloads)
		print(u"======================================")

init_env()
init_args()
init_dir_and_file()
init_dice()
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTSTP, signal_handler)
if view_cache:
	list_tag()
else:
#	scrapy_images()
	try:
		scrapy_images()
	except KeyboardInterrupt:
		save_dice()
		print(u"Unnatural exit.")
	except:
		save_dice()
		print(u"Unkown exception.")
	else:
		save_dice()
		print(u"Goodbye.")

