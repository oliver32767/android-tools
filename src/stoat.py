'''
Created on Oct 15, 2011

@author: waxwing

this should be run with plain old python2, not monkeyrunner
'''

import os, sys, commands

class Config():
    '''
    This class implements an interface to a config file.
    The constructor takes a path to a config file which is parsed line by line
    and data is added to a dictionary.
    '''
    
    def castValue(self, value):
        '''Takes a value and casts in into the most appropriate type: string,
        int, or float. castValue ignores strings quoted with either ' or "
        '''
        
        try:
            value = value.strip()
            if (value[0] in ['"', "'"]) and (value[-1] in ['"', "'"]):
                # this means the value is surrounded by quotes, don't recast
                return value[1:-1]

        except(AttributeError):
            # value doesn't have a strip method, ignore
            pass
        
        try:
            rv = int(value)
        except(ValueError):
            try:
                rv = float(value)
            except(ValueError):
                rv = value
        return rv
    
    def __init__(self, filename):
        '''
        Populate a dictionary based on data in filename.
        In filename, %s is replaced with the user's $HOME path.
        config file syntax:
        -------------------------------------------------------
        foo: 12
        bar: spam, eggs
        [SUBSECTION]
        boz: scaggs
        
        will yield the following data structure:
        {'MAIN': {'foo':12,'bar':['spam', 'eggs']}, 'SUBSECTION': {'boz': 'scaggs'}}
        
        if there is only one subsection, then the associated dictionary becomes top-level
        '''
        
        try:
            filename = filename % os.getenv('HOME')
        except(TypeError):
            # there wasn't a %s
            pass
        
        sec = 'MAIN' # default section header
        self.values = {sec: {}}
        try:
            f = open(filename, 'r')
            
            for line in f.readlines():
                if line.strip()[0] == '[': # section header
                    sec = line.strip()[1:-1]
            
                elif (line.strip() != '') and (line.strip()[0] != '#'): 
                    # ignore blank lines and lines beginning with '#'
                    # key : val
                    key = self.castValue(line[:line.find(':')].strip())
                    
                    val = line[line.find(':') + 1:]
                
                    if val.find(',') == -1:
                        val = self.castValue(val)
                    else:
                        # there's a comma in the value, split it into a list
                        newval = []
                        for v in val.split(','):
                            newval.append(self.castValue(v))
                        val = newval
                        

                    # now we add val to the appropriate section in the main dict
                    try:
                        self.values[sec][key] = val
                    except (KeyError):
                        # if we're here, that means the key doesn't exist
                        # so we need to initialize it first
                        self.values[sec] = {}
                        self.values[sec][key] = val
            f.close()
                
        except(IOError):
            # file not found, leave values{} empty
            self.values = {}
        
        
    def value(self, key, section = 'MAIN'):
        '''Safe access to values in the dictionary'''
        try:
            rv = self.values[section][key]
        except(KeyError):
            rv = None
        return rv

def adb(args):
    cmd = 'adb ' + args
    return commands.getoutput(cmd)

c = Config('%s/.stoat.conf')
print(c.values)