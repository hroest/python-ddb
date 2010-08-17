import perl
perl.eval( "use lib './' ")
perl.require( 'DDB::GENE' )
perl.require( 'DDB::PROTEIN' )
perl.require( 'DDB::SEQUENCE' )
perl.require( 'DDB::PEPTIDE' )


import sys
sys.path.append( '/home/hr/projects/aebersold/pyperl_project/code/')
import config

obj = perl.callm("new", 'DDB::GENE'  )
obj[ '_ensembl_stable_id' ] = 9
obj[ '_experiment_key' ] = 42
obj.addignore_setid()


myobj = get_object( 'DDB::GENE')
myobj._experiment_key 

def get_object( name ):
    obj = perl.callm("new", name )
    def __getattribute__(self,name):
        attr = object.__getattribute__(self, name)
        if hasattr(attr, '__call__'):
            def newfunc(*args, **kwargs):
                print('before calling %s' %attr.__name__)
                attr(*args, **kwargs)
                print('done calling %s' %attr.__name__)
            return newfunc
        else:
            return attr
    def attr_not_found(self, name):
        print "I did not find it"
        print name
    obj.__getattr__ = attr_not_found
    return obj


myobj = PerlWrapper( 'DDB::GENE')
myobj.test
myobj.test(5)
myobj.ref.__dic__

myobj = PerlWrapper( 'DDB::GENE')
#myobj[ '_ensembl_stable_id' ] 
#myobj._ensembl_stable_id
myobj.get_ensembl_stable_id()
myobj.set_ensembl_stable_id(9)
myobj.get_ensembl_stable_id()
myobj._ensembl_stable_id = 42
myobj.get_ensembl_stable_id()


myobj = PerlWrapper( 'DDB::PROTEIN')


###########################################################################
## Object abstraction
###########################################################################
#
# In order to get a variable, one can use the obj.get_x function
#
# In order to set a variable in the Perl object, one can use the
# obj.set_x functions, the obj.x = expression or obj.ref['x'] = 
#
# In order to set a variable in the Python object, one can only use
# obj.__dict__['x'] = 

class AccessError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr('Access denied for value ' + self.value + 'Make sure it is writeable.')


debug = True
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
        if debug: print('called init ' + name)
        ref = perl.callm("new", name )
        self.__dict__[ 'ref' ] = ref
    def __getattr__(self,name):
        """intercepts all get calls to attributes that are NOT in self.__dict__
        may either be an attribute of the Perl object or a function of it"""
        if debug: print('try to get %s' % name)
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
        if debug: print('try to set %s to %s' % (name, value))
        #We have to search in the attribute __dict__ of the object
        if self.__dict__.has_key(name): # or name == 'ref':
            #try to set the attribute first in the inner Python object
            self.__dict__[ name ] = value
        #and in the attribute __dict__ of the class
        elif self.__class__.__dict__.has_key(name):
            if debug: print "try to use the class __dict__"
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
        for attr in classdict['_attr_data']:
            print attr
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
                    print('getter found for ' + attr)
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

def ddb_setter_getter(aClass):
    #doesnt quite work, its easier to do it before dictproxy object is in place
    ##print "ddb_setter_getter decorator for %s" % aClass.__name__
    ##attr_data = aClass._attr_data
    ##classdict = aClass.__dict__
    ##print aClass.__dict__
    ##for attr in attr_data:
    ##    print attr
    ##    if attr_data[attr][1].find('read')!=-1 and not classdict.has_key('get'+attr):
    ##        exec( "def getter(self): return self.%s" % attr)
    ##        setattr( aClass, 'get' + attr, getter)
    ##    if attr_data[attr][1].find('write') != -1:
    ##        exec( "def setter(self, value): self.%s = value" % attr)
    ##        setattr( aClass, 'set' + attr, setter)
    ##        exec( 'def set%s(self, val): self.%s = val' % (attr, attr))
    ##        #
    ##        #easy access to properties
    ##        setattr( aClass, attr[1:], property(getter, setter) )
    ##        #exec( "if not classdict.has_key('set%s'):classdict['set%s'] = set%s" % (attr, attr, attr))
    ##    #exec( 'print get%s' % (attr ))
    ##return aClass

class ddbTestObject(PerlWrapper):
    """DDB test object."""
    __metaclass__ = ddb_api
    __table__ = 'test'
    _attr_data = {
            '_id' : ['','read/write'],
            '_test' : [0,'read/write'],
            '_test_readonly' : [0,'read']
    }
    def __init__(self):
        PerlWrapper.__init__( self, 'DDB::PROTEIN')
        for attr in self.__class__._attr_data:
            #self.__dict__[ attr ] = _attr_data[attr][0]
            #exec("self.%s = Protein._attr_data['%s'][0]" % (attr, attr) ) 
            setattr( self, attr, self.__class__._attr_data[attr][0] )
            pass
        self._sequence_loaded = False
    def get_id(self): 
        print('here in own test id fxn')
        return self._id
    id = property(fget=get_id )
    def getx(self):
        print('here get x')
        return self._x 
    def setx(self, val):
        print('here set x')
        self._x = val
    x = property(getx, setx)

class Protein(PerlWrapper):
    """DDB object for ddb.protein.
    .
    """
    #only add the metaclass if you want to create default set_ and get_
    #methods for the data below
    __metaclass__ = ddb_api
    __table__ = 'protein'
    _attr_data = {
            '_id' : ['','read/write'],
            '_sequence_key' : ['','read/write'],
            '_gene_key' : [0,'read/write'],
            '_protein_type' : ['','read/write'],
            '_experiment_key' : ['','read/write'],
            '_comment' : ['','read/write'],
            '_file_key' : ['','read/write'],
            '_mark_warning' : ['','read/write'],
            '_parse_key' : [0, 'read/write' ],
            '_probability' : [0,'read/write'],
            '_test' : [0,'read/write'],
            '_test_readonly' : [0,'read']
    }
    def __init__(self):
        PerlWrapper.__init__( self, 'DDB::PROTEIN')
        for attr in Protein._attr_data:
            #self.__dict__[ attr ] = _attr_data[attr][0]
            #exec("self.%s = Protein._attr_data['%s'][0]" % (attr, attr) ) 
            setattr( self, attr, self.__class__._attr_data[attr][0] )
            pass
        self._sequence_loaded = False
    def _load_sequence(self):
        self._sequence = Sequence(id=self.sequence_key)
        self._sequence.load()
        self._sequence_loaded = True
    def get_sequence(self):
        if not self._sequence_loaded: self._load_sequence()
        return self._sequence
    #
    #

class Sequence(PerlWrapper):
    """DDB object for ddbMeta.sequence.
    .
    """
    #only add the metaclass if you want to create default set_ and get_
    #methods for the data below
    __metaclass__ = ddb_api
    __table__ = config.commondb + '.sequence'
    _attr_data = {
        '_id' : [0,'read/write'],
        '_db' : ['','read/write'],
        '_ac' : ['','read/write'],
        '_ac2' : ['','read/write'],
        '_description' : ['','read/write'],
        '_marker' : ['','read/write'], # arbitrary marker
        '_sequence' : ['','read/write'],
        '_len' : ['','read/write'],
        '_reverse_sequence' : ['','read/write'],
        '_sha1' : ['','read/write'],
        #_molecular_weight' : [0,'read/write'],
        #_pi' : [0,'read/write'],
        '_comment' : ['','read/write'],
        '_insert_date' : ['','read/write'],
        '_timestamp' : ['','read/write'],
        '_ac' : ['','read/write'],
        '_debug' : [0,'read/write'],
        '_markary' : [[],'read/write'],
        '_markhash' : [{},'read/write'],
        '_is_markhash' : [0,'read/write'],
        '_is_marked' : [0,'read/write'],
        '_n_marked' : [0,'read/write'],
        '_tmp_annotation' : [0,'read/write']
     }
    def __init__(self, **kwargs):
        PerlWrapper.__init__( self, 'DDB::SEQUENCE')
        for attr in Sequence._attr_data:
            #go through all attributes and do the following
            #A set to kwargs if given as keyword
            #B else set to value of the caller object if possible
            #C else set to default value
            #self.__dict__[ attr ] = _attr_data[attr][0]
            exec("self.%s = Sequence._attr_data['%s'][0]" % (attr, attr) ) 
            pass
        if debug: print "init sequence object"
        for k in kwargs:
            if '_' + k in self.__class__._attr_data.keys(): 
                if debug: print(k + ' is in _attr_data')
                setattr(self, '_' + k, kwargs[k] )
            if debug: print(k)

class Peptide(PerlWrapper):
    """DDB object for ddbMeta.sequence.
    .
    """
    #only add the metaclass if you want to create default set_ and get_
    #methods for the data below
    __metaclass__ = ddb_api
    __table__ = 'peptide'
    __obj_table_link__ = 'protPepLink';
    _attr_data = {
        '_id' : [0,'read/write'],
        '_peptide' : ['','read/write'],
        '_peptide_type' : ['','read/write'],
        '_experiment_key' : [0,'read/write'],
        '_parent_sequence_key' : ['','read/write'],
        '_pi' : [0,'read/write'],
        '_molecular_weight' : [0,'read/write'],
        '_file_key' : [0,'read/write']
     }
    def __init__(self, **kwargs):
        PerlWrapper.__init__( self, 'DDB::PEPTIDE')
        for attr in self.__class__._attr_data:
            #go through all attributes and do the following
            #A set to kwargs if given as keyword
            #B else set to value of the caller object if possible
            #C else set to default value
            #setattr( self, attr, self.__class__._attr_data[attr][0] )
            setattr( self, attr, self.__class__._attr_data[attr][0] )
            pass
        if debug: print "init peptide object"
        for k in kwargs:
            if '_' + k in self.__class__._attr_data.keys(): 
                if debug: print(k + ' is in _attr_data')
                setattr(self, '_' + k, kwargs[k] )
            if debug: print(k)


class TestProteinFunctions(unittest.TestCase):
    def setUp(self):
        self.prot = Protein

def test_create_protein():
    p = Protein()

def test_addignore_protein():
    p = Protein()
    p.set_sequence_key( 43 )
    p.set_experiment_key( 89 )
    p.set_parse_key( 1 )
    p.set_probability( 0.6 )
    p.addignore_setid()
    print('Done addignore TEST')
    return p

def test_get_protein():
    p = test_addignore_protein()
    assert int( p.id ) == 49
    assert p.id  == p._id
    assert p.id  == p.get_id()
    assert p.id  == p.ref['_id']
    print('Done get TEST')

def test_set_protein():
    p = test_addignore_protein()
    p.id = 20
    assert int(p.ref['_id']) == 20
    p._id = 21
    assert int(p.ref['_id']) == 21
    p.set_id(22)
    assert int(p.ref['_id']) == 22
    p.ref['_id'] = 23
    assert int(p.ref['_id']) == 23
    print('Done set TEST')

def test_sequence_protein():
    p = Protein()
    p.set_sequence_key( 42 )
    p.set_experiment_key( 89 )
    p.set_parse_key( 1 )
    p.set_probability( 0.6 )
    p.addignore_setid()
    s = p.get_sequence()
    assert s.get_sequence() == 'PROTEIN'
    assert int( s.get_position( s.get_sequence() ) ) == 1
    return s

def test_read_only_attributes():
    test = ddbTestObject()
    test.get_test_readonly()
    try:
        test.set_test_readonly()
        assert False
    except Exception:pass
    test.test_readonly
    try:
        test.test_readonly = 8
        assert False
    except AccessError: pass

def test_all_protein():
    test_create_protein()
    test_addignore_protein()
    test_get_protein()
    test_set_protein()
    test_sequence_protein()
    test_read_only_attributes()
    print('Done all TEST')

debug=False
test_all_protein()
debug=True


p = test_addignore_protein()
s = test_sequence_protein()

list( p.get_ids() ) 

pep = Peptide()
pep = Peptide(peptide='PEPTIDE',experiment_key=89,peptide_type='bioinfo')
pep.addignore_setid()
list( pep.get_ids() ) 


#is that still used?
myhash = perl.get_ref( '%' )
h = {'id':  1}
myhash.update( h )
#perl.callm( 'get_object', pep, myhash)

#is that still used?
myhash = perl.get_ref( '%' )
h = {'peptide':  'PEPTIDE', 'experiment_key' : 89}
myhash.update( h )
ex = perl.callm( 'exists', pep.ref , myhash)
ex = perl.callm( 'exists', pep.ref , peptide='PEPTIDE', experiment_key=89)
perl.callm( 'exists', pep.ref , h)



