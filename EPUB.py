import zipfile
import os
import zlib
#import sys
#import getopt
import shutil
from mako.template import Template #http://www.makotemplates.org/


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
	#self.acceptable  : files with this extention will be
	#tuple				personalized when self.personalize()
	#					is run. This should be changed if 
	#					other file formats are needed.
	#
	###########################################################
	def __init__(self, path):
		path = os.path.abspath(path)
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
		#self.filename = path[last:]
		self.baseparent = path[0:path.rfind('/')]
		self.log = list()
		self.acceptable = (
			'.xhtml',
			'.html',
			'.xml',
			'.js',
			'.css'
		)

	#self.compile() uses the base file to create an EPUB file.
	# It accomplishes this by creating a zip file where the
	# mimetype will be uncompressed and other files will be
	# compressed with standard zip compression. This is the 
	# EPUB 3 standard.
	#
	# RETURNS STRING: name of epub file created.
	def compile(self):

		#Create new EPUB file, overwirte old EPUB from the same files
		try:
			loc = self.tempdir
		except:
			loc = self.base

		epub = zipfile.ZipFile(loc + '.epub', mode ='w')

		#Fill new EPUB zip file with all of the pages and whatnot.
		start = len(loc) + 1
		for root, dirs, files in os.walk(loc):
		        for file in files:
		            unzipped = os.path.join(root, file)
		            if file[0] == '.':
		                self.log.append('Filtered: ' + file)
		                continue
		            if file == 'mimetype':
		                epub.write(unzipped, arcname=root[start:] + file)
		            else:
		                epub.write(unzipped, arcname=root[start:] + '/' + file, compress_type=zipfile.ZIP_DEFLATED)
		            self.log.append('Wrote: ' + root[start:] + '/' + file)
		epub.close()
		return loc + '.epub'

	def personalize(self, **data):
		self.tempdir = self.baseparent + '/temp'
		if not os.path.exists(self.tempdir):
			os.makedirs(self.tempdir)

		start = len(self.base) + 1
		for root, dirs, files in os.walk(self.base):
			for file in files:
				
				last = file.rfind('.')

				newcopy = self.tempdir+ '/' + root[start:] + '/' + file

				if not os.path.exists('../' + newcopy):
					try:
						os.makedirs(os.path.dirname(newcopy))
					except OSError:
						pass
				
				#Only some files should be personalized
				#Change the files in self.acceptable
				if file[last:] in self.acceptable:
					template = Template(filename=os.path.join(root, file))
					output = template.render(**data)

					copy = open(newcopy, 'w')
					copy.write(output)
					copy.close()
				else:
					shutil.copy(os.path.join(root,file), newcopy)



		return self.tempdir

				#find some other way to get the middle dirs#####################################################



				


			#print(root)
			
			#template = Template(filename=unzipped_path)
			#rendered = template.render()

	
if __name__ == "__main__":

	epub = EPUB('example')

	epub.personalize(name='Hayden')
	epub.compile()

	#os.system('open \''+ epub.compile(name='Hayden') +'\'')


	for ele in epub.log:
		print(ele)