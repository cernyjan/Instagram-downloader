# -*- coding: utf-8 -*-
# čžřě+áýčíáý+í

"""
name: Instagram-downloader -- Downloader for Instagram photos in full resolution 
autor: Černý Jan
email: cerny.jan@hotmail.com
version: 0.1
license: viz. LICENSE
"""

import ctypes
from time import sleep
import urllib2, json
import datetime
import os
from sys import exit
import os.path
from sys import argv


def test_connection():
	"""
	Checking the functional connection to the Internet
	query 'https://www.instagram.com'
	if unsuccessful - retries after 10s
	"""
	connect = True
	cycle = 2
	while connect:
		try:
			con = urllib2.urlopen("https://www.instagram.com")
			con.read()
			connect = False
			print ". . . connected . . ."
			return True
		except IOError:
			print "failed connection of internet"
			print "repeat attempt\n"
			if cycle > 0:
				cycle -= 1
				sleep(10)
			else:
				return False


def get_media_json(url):
	req = urllib2.Request(url)
	opener = urllib2.build_opener()
	try:
		f = opener.open(req)
	except urllib2.HTTPError, err:
		if err.code == 404:
			exit("Sorry, this page isn't available")
		else:
			raise
	return json.loads(f.read())


def get_file_url(url):
	file_url = url.split('?')[0]
	file_url = file_url.replace("/s320x320", "")
	return file_url


def save_file(folder, created_time, url):
	file_name = datetime.datetime.fromtimestamp(int(created_time)).strftime('%Y-%m-%d %H:%M:%S') + ".jpg"
	u = urllib2.urlopen(url)
	f = open(folder + "/" + file_name, 'wb')
	meta = u.info()
	file_size = int(meta.getheaders("Content-Length")[0])
	print "\nDownloading: %s Bytes: %s" % (file_name, file_size)

	file_size_dl = 0
	block_sz = 8192
	while True:
		buffer = u.read(block_sz)
		if not buffer:
			break

		file_size_dl += len(buffer)
		f.write(buffer)
		status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
		status = status + chr(8)*(len(status)+1)
		print status,

	f.close()


def download_and_save(data, folder):
	items_index = 0
	for item in data['items']:
		file_url = get_file_url(data['items'][items_index]['images']['low_resolution']['url'])
		
		created_time = data['items'][items_index]['created_time']
							
		save_file(folder, created_time, file_url)

		items_index = items_index + 1

def main():
	err = False
	loop = True
	first = True
	MAX_ID = 0
	
	print "\r"
	print "*************************************************************"
	print "Instagram downloader v0.1 \t author: Černý Jan \t 2016"
	print "*************************************************************"
	print "\r"

	#checking parameters when you run
	if len(argv) < 2:
		print "application has to run with some parameters !!"
		print "for help put '-help' parameter"
		print "and try again"
		print "\n"
		exit()

	#help
	if argv[1] == "-help":
		print "HELP"
		print "===="
		print "example of use: python instagram-downloader.py user001"
		print "\n"
		exit()
		
	if len(argv) < 2:
		err = True
	else:
		user = argv[1]
		
	if not err:
		#internet connection test
		if test_connection():
			pass
		else:
			exit("app down")

		if not os.path.exists(user):
			os.makedirs(user)
		
		url = "https://www.instagram.com/" + user + "/media/"
		
		while loop:		
			data = get_media_json(url)
			items_count = len(data['items'])

			if items_count == 0:
				if first:
					exit("Sorry, nothing to download")
				else:
					loop = False
					break
			elif items_count == 20:
				MAX_ID = data['items'][(items_count - 1)]['id']
				first = False
			else:
				loop = False
			
			download_and_save(data, user)

			url = "https://www.instagram.com/" + user + "/media/?max_id=" + MAX_ID


		path = user
		print "\n\nTotal: " + str(len([f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))])) + " photo(s)"
		exit("--successfully finished--")
	else:
		print "application has to run with some parameters !!"
		print "for help put '-help' parameter"
		print "and try again"
		exit()     



if __name__ == '__main__':
	#changing the name of a running process for a better overview of the means utilized
	LIBC = ctypes.CDLL('libc.so.6')
	PROC_NAME = "000-Instagram-downloader"
	LIBC.prctl(15, '%s\0' %PROC_NAME, 0, 0, 0)
	#a delay of 1s
	sleep(1)
	
	#main thread
	main()