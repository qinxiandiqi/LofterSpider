#!/usr/bin/python
# -*- coding:utf8 -*-

import urllib2
import re
import os
import argparse
import thread
import time
import pickle

from bs4 import BeautifulSoup


all_downloads = 0
base_dir = u"atlas_images"
setting_dir = u'setting'
keep_working = True
max_page_error_times = 3
currrent_page_error_times = 0

main_domain = r'http://girl-atlas.com/'
tag_domain = r'http://girl-atlas.com/t/'
target_url = main_domain

group_dice = {}
girl_dice = {}
group_dice_file = u'group_dice'
girl_dice_file = u'girl_dice'

def init_args():
	global base_dir, max_page_error_times
	parse = argparse.ArgumentParser()
	parse.add_argument('-d', '--dir', dest='basedir', type=str,
		nargs='?', const=u"images", default=u"atlas_images",
		help='The base dir to save image, default is images')
	parse.add_argument('-m', '--max', dest='maxtimes', type=int,
		nargs='?', const=3, default=3,
		help='The max times to try next page when the current page get fail, default is 3')
	args = parse.parse_args()
	base_dir = args.basedir
	max_page_error_times = args.maxtimes
	print(u"\n======================================================================")
	print(u"Progress Setting:")
	print(u"1.Save images to %s dir" % base_dir)
	print(u"2.Max type next page time is %s." % max_page_error_times)
	print(u"======================================================================\n")

def init_dir_and_file():
	global base_dir, setting_dir, group_dice_file, girl_dice_file
	currentPath = os.getcwd()
	base_dir = os.path.join(currentPath, base_dir)
	if not os.path.isdir(base_dir):
		os.mkdir(base_dir)
	setting_dir = os.path.join(currentPath, setting_dir)
	if not os.path.isdir(setting_dir):
		os.mkdir(setting_dir)
	group_dice_file = setting_dir + "/" + group_dice_file
	girl_dice_file = setting_dir + "/" + girl_dice_file

def init_dice():
	global group_dice, girl_dice, group_dice_file, girl_dice_file
	try:
		with open(group_dice_file, 'r') as group_file:
			group_dice = pickle.load(group_file)
	except:
		print(u"Get group dice cache file fail, using null dice.")
		group_dice = {}
	try:
		with open(girl_dice_file, 'r') as girl_file:
			girl_dice = pickle.load(girl_file)
	except:
		print(u"Get girl dice cache file fail, using null dice.")
		girl_dice = {}	

def save_dice():
	global group_dice, girl_dice, group_dice_file, girl_dice_file
	#try:
	with open(group_dice_file, 'w') as group_file:
		pickle.dump(group_dice, group_file)
	#except:
		#print(u"Sorry,save group dice fail.")
	#try:
	with open(girl_dice_file, 'w') as girl_file:
		pickle.dump(girl_dice, girl_file)
	#except:
		#print(u"Sorry,save girl dice fial.")

def input_handle():
	global keep_working
	print(u"Now start scrapy progress,you can type ENTER key to stop anytime...\n")
	raw_input()
	keep_working = False
	print(u"Handle the working progress, please wait...\n")
	
def scrapy_images():
	global all_downloads, base_dir, keep_working, max_page_error_times, current_page_error_times, group_dice, girl_dice, target_url
	keep_working = True 
	#thread.start_new(input_handle,())
	time.sleep(1)
	page_url = target_url
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
					tag_name = u"default"
					atlas_id = tag_name
					print tags[i]
					continue
				if girl_dice.has_key(tag_name):
					atlas_id = tag_name
					break
				elif group_dice.has_key(tag_name):
					if i == 0:
						atlas_id = tag_name
				else:
					tag_code = tags[i].get('href').split('/')[-1]
					your_choose = raw_input((tag_name + " is a girl's name?(y/n):").encode('utf-8'))
					if your_choose.strip().lower() == 'y':
						girl_dice.setdefault(tag_name, tag_code)
						atlas_id = tag_name
						break
					else:
						group_dice.setdefault(tag_name, tag_code)
						if i == 0:
							atlas_id = tag_name
			print(atlas_id)
			
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
					image_content = urllib2.urlopen(image_url).read()
				except:
					print "Get image fail:" + image_url
					continue
				image_save_path = target_dir_path + "/" + image_url.split("/")[-1].split("!")[0]
				if os.path.exists(image_save_path):
					print "Image is existed:" + image_save_path
					continue
				try:
					with open(image_save_path, 'wb') as datas:
						datas.write(image_content)
				except:
					print "Save image fail:" + image_save_path
					continue
				all_downloads = all_downloads + 1
				print "Save image success:" + image_save_path
		print u"Parse this page  %s image groups. " % image_group_count
		keep_working = False
	else:
		print u"======================================"
		print u"Progress Done!"
		print u"All download %s images" % ALL_DOWNLOADS
		print u"======================================"

init_args()
init_dir_and_file()
#try:
scrapy_images()
save_dice()
#except KeyboardInterrupt:
#	print "Unnatural exit.\nIf you want to cancel the progress,please type ENTER key."
#	save_dice()
#except:
#	print "Unkown exception."
#	save_dice()
	
