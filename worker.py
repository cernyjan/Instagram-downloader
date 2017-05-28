#!/usr/bin/python
# -*- coding: utf-8 -*-
# čžřě+áýčíáý+í

import urllib2
import os.path
import os
import datetime

class Worker(object):
		def __init__(self, images, folder):
			self.images = images
			self.folder = folder

		def validate_type(self, var, varType):
			if isinstance(var, varType):
				return True
			else:
				return False

		def folder_exists(self, folder):
			if os.path.exists(folder):
				return True
			else:
				return False

		def create_folder(self, folder):
			os.makedirs(folder)

		def save_file(self, folder, url, created_time):
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

		def work(self):
			for image in self.images:
				if not self.folder_exists(self.folder):
					self.create_folder(self.folder)
				else:
					self.save_file(self.folder, image[0], image[1])
				self.save_file(self.folder, image[0], image[1])