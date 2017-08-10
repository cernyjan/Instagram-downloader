#!/usr/bin/python
# -*- coding: utf-8 -*-
# čžřě+áýčíáý+í

"""
This file is part of Instagram downloader.
"""

import urllib2
import json
import sys
import time


class Builder(object):
	def __init__(self, user, debug):
		self.user = user
		self.images = []
		self.number_of_images = -1
		self.last_id = ""
		self.more_available = False
		self.debug = debug
		if self.debug:
			print "builder OK"

	def validate_type(self, var, varType):
		if isinstance(var, varType):
			return True
		else:
			return False

	def transform_file_url(self, url):
		#orig: old - https://scontent-frt3-1.cdninstagram.com/t51.2885-15/s320x320/e35/15875894_1508741892486869_7973405638820626432_n.jpg?ig_cache_key=MTQyNjU4NDM4ODgxNjIzNjIzMQ%3D%3D.2 or new - https://scontent-frt3-1.cdninstagram.com/t51.2885-15/s320x320/e35/c135.0.809.809/14723725_1842050342674900_2393076900256808960_n.jpg?ig_cache_key=MTQ1MDAyNTg3MDg3Mjk3Njc3MQ%3D%3D.2.c
		file_url = url.split('?')[0]
		file_url = file_url.replace("/s320x320", "")
		file_url = file_url.split('/')
		if len(file_url) == 6:
			file_url = file_url[0] + "//" + file_url[2] + "/" + file_url[3] + "/" + file_url[4] + "/" + file_url[5]
		elif len(file_url) == 7:
			file_url = file_url[0] + "//" + file_url[2] + "/" + file_url[3] + "/" + file_url[4] + "/" + file_url[6] 
		else:
			exit("Sorry, unexpected error occurred")
		#new: https://scontent-frt3-1.cdninstagram.com/t51.2885-15/e35/14723725_1842050342674900_2393076900256808960_n.jpg
		return file_url

	def get_media_json(self, url):
		req = urllib2.Request(url)
		opener = urllib2.build_opener()
		try:
			f = opener.open(req)
		except urllib2.HTTPError, err:
			if err.code == 404:
				exit("Sorry, this page isn't available")
			else:
				raise
		#TODO: add prevent of socket.error: [Errno 104] Connection reset by peer
		#TODO: add prevent of socket.error: [Errno 10054] An existing connection was forcibly closed by the remote host
		return json.loads(f.read())

	def set_last_id(self, last_id):
		if self.validate_type(last_id, str):
			self.last_id = last_id
		else:
			pass

	def get_last_id(self):
		return self.last_id 

	def set_images(self):
		url = "https://www.instagram.com/" + self.user + "/media/"
		loop = True
		if self.debug:
			print "processing ",
		while loop:  
			number_of_images = self.get_number_of_images() 
			data = self.get_media_json(url)
			items_count = len(data['items'])

			if items_count == 0:
				if first:
					exit("Sorry, nothing to download")
				else:
					loop = False
					break
			elif items_count == 20:
				self.set_last_id(str(data['items'][(items_count - 1)]['id']))
				first = False
			else:
				loop = False

			items_index = 0
			for item in data['items']:
				file_url = self.transform_file_url(data['items'][items_index]['images']['low_resolution']['url'])
				created_time = data['items'][items_index]['created_time']
				image = [file_url, created_time]
				if not any(created_time in i for i in self.get_images()):
					self.images.append(image)
					if self.debug:
						sys.stdout.write(".")
						sys.stdout.flush()
					#time.sleep(.05)
				items_index = items_index + 1

			self.set_number_of_images(len(self.images))

			url = "https://www.instagram.com/" + self.user + "/media/?max_id=" + self.get_last_id()

			if number_of_images == self.get_number_of_images():
				loop = False
		if self.debug:
			sys.stdout.write("\n")
			sys.stdout.flush()
				
	def get_images(self):
		return self.images

	def set_number_of_images(self, number):
		if self.validate_type(number, int):
			self.number_of_images = number
		else:
			pass  

	def get_number_of_images(self):
		return self.number_of_images
