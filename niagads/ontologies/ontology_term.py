import logging
from os.path import basename

from . import annotation_property_types, ANNOTATION_PROPERTIES
from ..utils.list import list_to_string

class OntologyTerm:
    def __init__(self, iri, debug=False):
        self.logger = logging.getLogger(__name__)
        self.__debug = debug
        
        self.__iri = iri
        self.__id = basename(iri).replace(':', '_')
        self.__term = None
        self.__annotationProperties = {}
        self.__subclass_of = None
        self.__synonyms = None
        self.__dbRefs = None
        self.__includeComments = False # TODO: flag to include comments in output
       
    def include_comments(self, includeComments=True):
        self.__includeComments = includeComments
     
    def debug(self, debug=True):
        self.__debug = debug   
        
    def add_db_ref(self, value):
        value = value.replace(': ', ':')
        if self.__dbRefs is None:
            self.__dbRefs = [value]
        else:
            self.__dbRefs.append(value)
       
            
    def add_synonym(self, value):
        if self.__synonyms is None:
            self.__synonyms = [value]
        else:
            self.__synonyms.append(value)
            
        
    def set_is_a(self, relationships):
        self.__subclass_of = relationships
        
    def get_db_refs(self, asStr=False):
        if self.__dbRefs is None:
            return None      
        return '//'.join(self.__dbRefs) if asStr else self.__dbRefs
        
    def get_synonyms(self, asStr=False):
        if self.__synonyms is None:
            return None   
        return '//'.join(self.__synonyms) if asStr else self.__synonyms
        
    def is_a(self, asStr=False):
        if self.__subclass_of is None:
            return None  
        return '//'.join(self.__subclass_of) if asStr else self.__subclass_of
        
    def get_id(self):
        return self.__id
    
    def get_iri(self):
        return self.__iri
    
    def get_term(self):
        return self.__term
    
    def set_term(self, term):
        self.__term = term
        
    def get_annotation_properties(self):
        return self.__annotationProperties
            
    def in_namespace(self, namespace: str):
        if self.__id.startswith(namespace + '_'):
            return True
        else:
            return False
        
        
    def __str__(self):
        """str() wrapper

        Returns:
            tab delimited string of term and its annotations
        """
        values = [self.__id, self.__iri, self.__term]
        for prop in annotation_property_types():
            annotation = '//'.join(self.__annotationProperties[prop]) \
                if prop in self.__annotationProperties else None
            values.append(annotation)
    
        return list_to_string(values, nullStr='', delim='\t')
    
        
    def set_annotation_property(self, prop, value):
        if prop == 'label':
            self.set_term(value)
        else:
            propType = self.valid_annotation_property(prop, returnType=True)
            
            if propType == 'db_ref': 
                self.add_db_ref(value)
            if propType == 'synonym':
                self.add_synonym(value)
            else:    
                value = [value] # make everything a list
                if propType in self.__annotationProperties:
                    self.__annotationProperties[propType] = self.__annotationProperties[propType] + value
                else:
                    self.__annotationProperties[propType] = value
                
    
    def valid_annotation_property(self, property, returnType=False):
        for annotType, properties in ANNOTATION_PROPERTIES.items():
            if property in properties:
                return annotType if returnType else True
        
        # if can't be mapped:    
        if not returnType:
            return False
        else:
            raise KeyError('Annotation property: ' + property + ' not in reserved types.')
