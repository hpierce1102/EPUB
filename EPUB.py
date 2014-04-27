import zipfile
import os
import zlib
import sys
import getopt

class EPUB:
	###########################################################
	#self.fullpath    : the path, as provided in the arg      
	#string
	#
	#self.base        : the dir that houses the mimetype file
	#string 		    it will house all of the EPUB's files
	#
	#
	#self.baseparent  : parent dir of the above base.
	#string
	#
	#self.log         : list of all writes and filters the 
	#list               compiler creates
	#                   
	###########################################################
	def __init__(self, path):
		self.fullpath = path

		found = False
		notdir = False

		#attempt to find the top directory for the ebook.
		#This assumes that a META-INF folder exists (as per EPUB standard).
		while 1:
			try:
				for files in os.listdir(path):
					if files == 'META-INF':
						found = True
						break
			except OSError:
				if notdir == True:
					raise NameError('EPUB.__INIT__:No META-INF directory found.')
				notdir = True
			if found == True: break
			last = path.rfind('/')
			path = path[0:last]
		self.base = path
		self.filename = path[path.rfind('/') + 1:last]
		self.baseparent = path[0:path.rfind('/')]
		self.log = list()

	#self.compile() uses the base file to create an EPUB file.
	# It accomplishes this by creating a zip file where the
	# mimetype will be uncompressed and other files will be
	# compressed with standard zip compression. This is the 
	# EPUB 3 standard.
	#
	# RETURNS STRING: name of epub file created.
	def compile(self):

		#Create new EPUB file, overwirte old EPUB from the same files
		epub = zipfile.ZipFile(self.base + '.epub', mode ='w')

		#Fill new EPUB zip file with all of the pages and whatnot.
		start = len(self.base) + 1
		for root, dirs, files in os.walk(self.base):
		        for file in files:
		            if file[0] == '.':
		                self.log.append('Filtered: ' + file)
		                continue
		            if file == 'mimetype':
		                epub.write(os.path.join(root, file), arcname=root[start:] + file)
		            else:
		                epub.write(os.path.join(root, file), arcname=root[start:] + '/' + file, compress_type=zipfile.ZIP_DEFLATED)
		            self.log.append('Wrote: ' + root[start:] + '/' + file)
		epub.close()
		return self.base + '.epub'

if __name__ == "__main__":
	arg = getopt.getopt(sys.argv, '')
	try:
		dir = arg[1][1]
	except IndexError:
		sys.exit('Failed: No argument supplied')
	epub = EPUB(dir)
	os.system('open \''+ epub.compile() +'\'')
	#print(epub.base)
	#print(epub.filename)
	for ele in epub.log:
		print(ele)