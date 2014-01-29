#!/usr/bin/env python

from distutils.core import setup

# all the specifics are selected in setup.cfg
setup(name='pathagar',
	packages = ['pathagar',
		'pathagar.books',
		'pathagar.books.management',
		'pathagar.books.management.commands'
		],
	package_dir = {'pathagar':''},
	package_data = {'pathagar':[
        'static/images/*',
		'static/js/*',
		'static/style/*.css',
		'static/style/blueprint/*.css',
#		'static/style/blueprint/plugins/rtl/*.txt',
#		'static/style/blueprint/plugins/rtl/*.css',
		'static/style/blueprint/plugins/rtl/*.txt',
		'static/style/blueprint/plugins/link-icons/*.{txt,css}',
		'static/style/blueprint/plugins/link-icons/*.txt',
		'static/style/blueprint/plugins/link-icons/icons/*',
		'static/style/blueprint/plugins/fancy-type/*',
		'static/style/blueprint/plugins/buttons/*.txt',
		'static/style/blueprint/plugins/buttons/*.css',
		'static/style/blueprint/plugins/buttons/icons/*',
		'templates/*.html',
		'templates/registration/*',
		'templates/admin/*',
		'templates/books/*',
		'AUTHORS',
		'COPYING',
		'README.mkd',
		'requirements.pip',
		'settings.*',
		'setup.*',
		'books/fixtures/*',
		'books/templates/*',
		]}
	)

