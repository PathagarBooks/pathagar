# Copyright 2009 One Laptop Per Child
# Author: Sayamindu Dasgupta <sayamindu@laptop.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import zipfile
import tempfile
import os, os.path
from lxml import etree
import shutil

import epubinfo


class Epub(object):
    def __init__(self, _file):
        """
        _file: can be either a path to a file (a string) or a file-like object.
        """
        self._file = _file
        self._zobject = None
        self._opfpath = None
        self._ncxpath = None
        self._basepath = None
        self._tempdir = tempfile.mkdtemp()
        
        if not self._verify():
            print 'Warning: This does not seem to be a valid epub file'
        
        self._get_opf()
        self._get_ncx()
        
        opffile = self._zobject.open(self._opfpath)
        self._info = epubinfo.EpubInfo(opffile) 
        
        self._unzip()
        
    def _unzip(self):
        #self._zobject.extractall(path = self._tempdir) # This is broken upto python 2.7
        orig_cwd = os.getcwd()
        os.chdir(self._tempdir)
        for name in self._zobject.namelist():
            if name.startswith(os.path.sep): # Some weird zip file entries start with a slash, and we don't want to write to the root directory
                name = name[1:]
            if name.endswith(os.path.sep) or name.endswith('\\'):
                os.makedirs(name)
            else:
                self._zobject.extract(name)
        os.chdir(orig_cwd)

                
    def _get_opf(self):
        containerfile = self._zobject.open('META-INF/container.xml')
        
        tree = etree.parse(containerfile)
        root = tree.getroot()
        
        for element in root.iterfind('.//{urn:oasis:names:tc:opendocument:xmlns:container}rootfile'):
            if element.get('media-type') == 'application/oebps-package+xml':
                self._opfpath = element.get('full-path')
        
        if self._opfpath.rpartition('/')[0]:        
            self._basepath = self._opfpath.rpartition('/')[0] + '/'
        else:
            self._basepath = ''
            
        containerfile.close()


    def _get_ncx(self):
        opffile = self._zobject.open(self._opfpath)
        
        tree = etree.parse(opffile)
        root = tree.getroot()

        spine = root.find('.//{http://www.idpf.org/2007/opf}spine')
        tocid = spine.get('toc')

        for element in root.iterfind('.//{http://www.idpf.org/2007/opf}item'):
            if element.get('id') == tocid:
                self._ncxpath = self._basepath + element.get('href')
        
        opffile.close()

    def _verify(self):
        '''
        Method to crudely check to verify that what we 
        are dealing with is a epub file or not
        '''
        if isinstance(self._file, basestring):
            self._file = os.path.abspath(self._file)
            if not os.path.exists(self._file):
                return False
        
        self._zobject = zipfile.ZipFile(self._file)
        
        if not 'mimetype' in self._zobject.namelist():
            return False
        
        mtypefile = self._zobject.open('mimetype')
        mimetype = mtypefile.readline()
        
        if not mimetype.startswith('application/epub+zip'): # Some files seem to have trailing characters
            return False
        
        return True
    
    def get_basedir(self):
        '''
        Returns the base directory where the contents of the
        epub has been unzipped
        '''
        return self._tempdir
    
    def get_info(self):
        '''
        Returns a EpubInfo object for the open Epub file
        '''        
        return self._info

    def get_cover_image_path(self):
        if self._info.cover_image is not None:
            return os.path.join(self._tempdir, 'OEBPS', self._info.cover_image)
        else:
            return None

    def close(self):
        '''
        Cleans up (closes open zip files and deletes uncompressed content of Epub. 
        Please call this when a file is being closed or during application exit. 
        '''                
        self._zobject.close()
        shutil.rmtree(self._tempdir)
