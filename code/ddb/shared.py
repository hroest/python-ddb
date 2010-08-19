from ddb import config
from ddb import perl

debug = config.debug

class PerlWrapper(object):
    """Superclass for all DDB objects.
    #
    This class intercepts all set and get calls and passes them to the 
    internal PerlRef object "ref". It checks the functions on the Python
    object first and THEN the ones from the Perl object.
    """
    def __init__(self,name):
        #because ref is not defined yet, we need to 
        #set it over __dict__ instead of self.ref
        if debug: print('initalize an instance of ' + name)
        ref = perl.callm("new", name )
        self.__dict__[ 'ref' ] = ref
    def __getattr__(self,name):
        """intercepts all get calls to attributes that are NOT in self.__dict__
        may either be an attribute of the Perl object or a function of it"""
        if debug: print('__getattr__ trace: get %s' % name)
        #------------------------------------------------------
        #if debug: print(self.__class__)
        #if self.__class__.__dict__.has_key(name):
        #    if type( self.__class__.__dict__[name])  == property:
        #        if debug: print('property found!!') 
        #        return self.__class__.__dict__[name].fget( self )
        #    else: return self.__class__.__dict__[name] 
        #------------------------------------------------------
        if debug: print('try to get %s from Perl object' % name)
        try:
            #try to find the attribute in the inner Perl object 
            return self.ref[ name ]
        except KeyError:
            #try to find the function in the inner Perl object 
            return eval('self.ref.%s' % name)
    def __setattr__(self, name, value):
        """setattr is harder than getattr because we get all set calls,
        not just the failed ones. So we need to check first whether we 
        set a Python attribute / function"""
        if debug: print('__setattr__ trace: set %s to %s' % (name, value))
        #We have to search in the attribute __dict__ of the object
        if self.__dict__.has_key(name): # or name == 'ref':
            #try to set the attribute first in the inner Python object
            self.__dict__[ name ] = value
        #and in the attribute __dict__ of the class
        elif self.__class__.__dict__.has_key(name):
            if debug: print "use the class __dict__"
            #properties are special because we don't actually want to set them
            #but rather call the appropriate fset method
            if type( self.__class__.__dict__[name])  == property:
                if self.__class__.__dict__[name].fset == None:
                    raise AccessError(name)
                self.__class__.__dict__[name].fset( self, value)
            else: self.__class__.__dict__[name] = value
        else:
            if debug:print('try to set %s to %s in Perl object' % (name, value))
            self.ref[ name ] = value

class ddb_api(type):
    """Metaclass for all DDB objects.
    .
    This is the metaclass that reads the classes _attr_data hash and creates
    get_* and set_* methods for each element in the hash.
    Note that this assumes that writing rights always includes reading rights.
    """
    def __new__(meta, classname, supers, classdict):
        if debug: print('Create class ' + classname)
        for attr in classdict['_attr_data']:
            if debug: print('adding getters and settes for ' + attr)
            exec( "def getter(self): return self.%s" % attr)
            exec( "def setter(self, val): self.%s = val" % attr)
            if debug: 
                exec( "def getter(self): \
                print('called get%s'); return self.%s" % (attr, attr))
                exec( "def setter(self, val): \
                print('called set%s with %%s'%%val); \
                     self.%s = val" % (attr, attr))
            if classdict['_attr_data'][attr][1].find('read') != -1:
                if not classdict.has_key('get%s' % attr): 
                    classdict['get%s' % attr ] = getter
                else:
                    if debug: print('getter found for ' + attr)
                    getter = classdict['get%s' % attr ]
                classdict['%s' % attr[1:] ] = property(fget=getter)
            if classdict['_attr_data'][attr][1].find('write') != -1:
                if not classdict.has_key('set%s' % attr):
                    classdict['set%s' % attr] = setter
                    #classdict['%s' % attr[1:] ] = property(fset=setter)
                    #if not classdict.has_key('get%s' % attr):
                    #    classdict['%s' % attr[1:] ] = property(fget=getter, fset=setter)
                else:
                    setter = classdict['set%s' % attr]
                classdict['%s' % attr[1:] ] = property(fget=getter, fset=setter)
        classdict[ 'db_connection' ] = config.get_db_connector()
        return type.__new__(meta, classname, supers, classdict)


class AccessError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr('Access denied for value ' + self.value +
                    '. Make sure it is writeable.')

class AttributeMissingError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr('Attribute ' + self.value + 
                    ' is missing. Make sure it is there.')

