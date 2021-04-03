from os import system, remove
from os.path import join, exists
from shutil import copytree, rmtree
from zipfile import ZipFile

TOOL = 'xdelta3'

IMAGES = {
	# docker-image-name :: (os, extension)
	'ubuntu': ('linux_x86_64', ''),
	'i386/ubuntu': ('linux_i386', ''),
}

for image, (os, extension) in IMAGES.items():
	# info
	zip = '%s-%s.zip' % (TOOL, os)
	print('='*100)
	print('>>', 'BUILD', zip)
	print('>>', 'USING', image)
	print('='*100)
	print()
	
	# clean
	zip = join('build', zip)
	if exists(zip): remove(zip)
	if exists('temp'): rmtree('temp')
	
	# make
	copytree('xdelta3', 'temp')
	commands = [
		'cd src/temp',
		'apt update',
		'apt install -y make gcc g++',
		'apt install -y automake-1.15',
		'apt install -y libtool liblzma-dev',
		'ln -s automake-1.15 automake-1.14',
		'ln -s aclocal-1.15 aclocal-1.14',
		'autoreconf -i',
		'make clean',
		'bash configure',
		'make',
		'rm automake-1.14',
		'rm aclocal-1.14',
	]
	system('docker run -it -v "%%cd%%":/src/ %s bash -c "%s"' % (image, '; '.join(commands)))
	
	# copy
	exe = join('temp', TOOL + extension)
	with ZipFile(zip, 'w') as zip: zip.write(exe, arcname = TOOL + extension)
	rmtree('temp')
	print()
