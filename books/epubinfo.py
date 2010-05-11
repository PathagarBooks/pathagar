import os
from lxml import etree


class EpubInfo(): #TODO: Cover the entire DC range
    def __init__(self, opffile):
        self._tree = etree.parse(opffile)
        self._root = self._tree.getroot()
        self._e_metadata = self._root.find('{http://www.idpf.org/2007/opf}metadata')
        
        self.title = self._get_title()
        self.creator = self._get_creator()
        self.date = self._get_date()
        self.subject = self._get_subject()
        self.source = self._get_source()
        self.rights = self._get_rights()
        self.identifier = self._get_identifier()
        self.language = self._get_language()
        self.summary = self._get_description()
        
    
    def _get_data(self, tagname):
        element = self._e_metadata.find(tagname)
        return element.text

    def _get_description(self):
        try:
            ret = self._get_data('.//{http://purl.org/dc/elements/1.1/}description')
        except AttributeError:
            return None

        return ret

    def _get_title(self):
        try:
            ret = self._get_data('.//{http://purl.org/dc/elements/1.1/}title')
        except AttributeError:
            return None
        
        return ret
        
    def _get_creator(self):
        try:
            ret = self._get_data('.//{http://purl.org/dc/elements/1.1/}creator')
        except AttributeError:
            return None        
        return ret
        
    def _get_date(self):
        #TODO: iter
        try:
            ret = self._get_data('.//{http://purl.org/dc/elements/1.1/}date')
        except AttributeError:
            return None
        
        return ret

    def _get_source(self):
        try:
            ret = self._get_data('.//{http://purl.org/dc/elements/1.1/}source')
        except AttributeError:
            return None
        
        return ret

    def _get_rights(self):
        try:
            ret = self._get_data('.//{http://purl.org/dc/elements/1.1/}rights')
        except AttributeError:
            return None
        
        return ret

    def _get_identifier(self):
        #TODO: iter
        element = self._e_metadata.find('.//{http://purl.org/dc/elements/1.1/}identifier')            

        if element is not None:
            return {'id':element.get('id'), 'value':element.text}
        else:
            return None

    def _get_language(self):
        try:
            ret = self._get_data('.//{http://purl.org/dc/elements/1.1/}language')
        except AttributeError:
            return None
        
        return ret

    def _get_subject(self):
        try:
            subjectlist = []
            for element in self._e_metadata.iterfind('.//{http://purl.org/dc/elements/1.1/}subject'):
                subjectlist.append(element.text)
        except AttributeError:
            return None
        
        return subjectlist
