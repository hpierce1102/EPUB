import zipfile
import os
#import zlib
import shutil
import tempfile
from jinja2 import Template, Environment, FileSystemLoader

class EPUB:
    def __init__(self, path_to_EPUB):
        self.log = list()
        self.path = path_to_EPUB
        self.acceptable = (
            '.xhtml',
            '.html',
            '.xml',
            '.js',
            '.css'
        )
        self.jinja_env = Environment(loader=FileSystemLoader(searchpath='/'))

    def vaildate(self):
        #TO DO: Add a mechnicism that confirms the file is usable.
        pass

    #Compiles the unzipped EPUB from EPUB.path to an *.epub file. 
    def compile(self, output_location):
        epub = zipfile.ZipFile(output_location, mode ='w')

        #Fill new EPUB zip file with all of the pages and whatnot.
        start = len(self.path) + 1
        for root, dirs, files in os.walk(self.path):
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

    def personalize(self, **data):
        self.temp_dir = tempfile.TemporaryDirectory()
        
        start = len(self.path) + 1
        for root, dirs, files in os.walk(self.path):

            #Need to create directories to write files in.
            for dir in dirs:
                os.mkdir(os.path.join(self.temp_dir.name,root[start:], dir))

            for file in files:
                copy_path = os.path.join(self.temp_dir.name, root[start:], file)

                #Only some files should be personalized
                #Change the files in self.acceptable
                last = file.rfind('.')
                if file[last:] in self.acceptable:
                    template = self.jinja_env.get_template(os.path.abspath(root + '/' + file))
                    output = template.render(**data)
                    copy = open(copy_path, 'w')
                    copy.write(output)
                    copy.close()
                    print(file + ' output: ' + output)
                else:
                    shutil.copy(os.path.abspath(root + '/'  + file), copy_path)
                    print('Direct Copy: ' + copy_path)

        self.path = self.temp_dir.name

    def debug_walk_self(self):
        print('self.path: ' + self.path)
        print('listdir: ' + str(os.listdir(self.path)))
        for root, dirs, files in os.walk(self.path + '/'):
            try:
                print('root: ' + root)
                print('dirs: ', end='')
                print(dirs)
                print('file: ', end='')
                print(files)
                print()
            except UnicodeEncodeError:
                print()
                continue

    def close(self):
        try:
            self.temp_dir.cleanup()
        except:
            pass

if __name__ == "__main__":
    epub = EPUB('example')
    epub.personalize(name = 'Hayden')
    epub.compile('personal_document.epub')
    epub.close()
    
    for ele in epub.log:
        print(ele)
