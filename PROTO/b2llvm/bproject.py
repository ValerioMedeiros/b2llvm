from b2llvm.strutils import commas
import xml.etree.ElementTree as ET

class BProject:
    '''
    Class representing B projects settings.
    '''
    def __init__(self, name):
        '''
        Constructor, takes as input the path of a bproject.xml file.
        '''
        root = ET.parse(name).getroot()
        implements = root.findall("./developed")
        self.implement = { e.find("./machine").text:e.find("./implementation").text 
                           for e in implements }
        foreign = root.findall("./base")
        self.developed = self.implement.keys()
        self.base = { e.find("./machine").text for e in foreign }

    def is_developed(self, m):
        ''' Tests if a machine is a developed machine.
        
        Inputs:
        - m: a machine name
        Returns:
        True iff m is declared as developed.
        '''
        return m in self.developed

    def is_base(self, m):
        ''' Tests if a machine is a base machine.

        Inputs:
        - m: a machine name
        Returns:
        True iff m is declared as base.
        '''
        return m in self.base

    def has(self, m):
        ''' Tests if a machine belongs to a B project

        Inputs:
        - m: a machine name
        Returns:
        True if m is a developed or a base machine declared in project, 
        False otherwise.
        '''
        return self.is_developed(m) or self.is_base(m)

    def implementation(self, m):
        assert self.is_developed(m)
        return self.implement[m]

    def __str__(self):
        return ("developed = {" + commas(self.developed) + "}\n" + 
                "implement = {" + commas([ m + ":" + i for m,i in self.implement.items()]) + "}\n" +
                "base = {" + commas(self.base) + "}\n")
