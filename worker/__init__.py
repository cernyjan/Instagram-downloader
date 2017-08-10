#!/usr/bin/python
# -*- coding: utf-8 -*-
# čžřě+áýčíáý+í

"""
This file is part of Instagram downloader.
"""

import urllib2
import os.path
import os
import datetime
import sys
import time


class Worker(object):
		def __init__(self, images, folder, debug):
			self.images = images
			self.folder = folder
			self.debug = debug
			if self.debug:
				print "worker OK"

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
			file_name = datetime.datetime.fromtimestamp(int(created_time)).strftime('%Y-%m-%d_%H-%M-%S') + ".jpg"
			u = urllib2.urlopen(url)
			f = open(folder + "/" + file_name, 'wb')
			meta = u.info()
			file_size = int(meta.getheaders("Content-Length")[0])
			
			file_size_dl = 0
			block_sz = 8192
			while True:
				buffer = u.read(block_sz)
				if not buffer:
					break

				file_size_dl += len(buffer)
				f.write(buffer)
				if self.debug:
					status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
					status = status + chr(8)*(len(status)+1)
					sys.stdout.write(status)
					sys.stdout.flush()
				#time.sleep(.05)
			if self.debug:
				print "%s Bytes: %s OK" % (file_name, file_size)

			f.close()

		def work(self):
			for image in self.images:
				if not self.folder_exists(self.folder):
					self.create_folder(self.folder)
				else:
					pass
				self.save_file(self.folder, image[0], image[1])
