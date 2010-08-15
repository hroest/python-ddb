import perl
perl.eval( "use lib './' ")
perl.require( 'DDB::GENE' )
perl.require( 'DDB::PROTEIN' )

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

class PerlWrapper(object):
    """Superclass for all DDB objects.

    This class intercepts all set and get calls and passes them to the 
    internal PerlRef object "ref". It checks the functions on the Perl
    object first and THEN the ones from the Python object.
    """
    def __init__(self,name):
        #because ref is not defined yet, we need to 
        #set it over __dict__ instead of self.ref
        print('called init ' + name)
        ref = perl.callm("new", name )
        self.__dict__[ 'ref' ] = ref
    def __getattr__(self,name):
        print('try to get %s' % name)
        try:
            #try to find the attribute in the inner Perl object first
            return self.ref[ name ]
        except KeyError:
            try:
                #now try to find a function in the inner Perl object next
                return eval('self.ref.%s' % name)
            except perl.PerlError: pass
        print('try to get %s from Python object' % name)
        return object.__getattribute__(self, name)
    def __setattr__(self, name, value):
        print('try to set %s to %s' % (name, value))
        try:
            #try to find the attribute first in the inner Perl object
            self.ref[ name ] = value
        except KeyError:
            print('try to set %s to %s in Python object' % (name, value))
            self.__dict__[ name ] = value

class ddb_api(type):
    """Metaclass for all DDB objects.
    
    This is the metaclass that reads the classes _attr_data hash and creates
    get_* and set_* methods for each element in the hash.
    """
    def __new__(meta, classname, supers, classdict):
        #print classdict['_attr_data']
        for attr in classdict['_attr_data']:
            print attr
            if classdict['_attr_data'][attr][1].find('read') != -1:
                exec( "def get%s(self): return self.%s" % (attr, attr))
                exec( "if not classdict.has_key('get%s'): classdict['get%s'] = get%s" % (attr, attr, attr))
            if classdict['_attr_data'][attr][1].find('write') != -1:
                exec( 'def set%s(self, val): self.%s = val' % (attr, attr))
                exec( "if not classdict.has_key('set%s'):classdict['set%s'] = set%s" % (attr, attr, attr))
            #exec( 'print get%s' % (attr ))
        return type.__new__(meta, classname, supers, classdict)

class Protein(PerlWrapper):
    """DDB object for ddb.protein.

    .
    """
    #only add the metaclass if you want to create default set_ and get_
    #methods
    __metaclass__ = ddb_api
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
            '_test' : [0,'read/write']
    }
    def __init__(self):
        PerlWrapper.__init__( self, 'DDB::PROTEIN')
        for attr in Protein._attr_data:
            #self.__dict__[ attr ] = _attr_data[attr][0]
            exec("self.%s = Protein._attr_data['%s'][0]" % (attr, attr) ) 
            pass
    def get_id(self): 
        print('here in own protein id fxn')
        return self._id


p = Protein()
p.set_sequence_key( 42 )
p.set_experiment_key( 1 )
p.set_parse_key( 1 )
p.set_probability( 0.6 )
p.addignore_setid()
p.get_sequence_key()

sequence = p.get_sequence()
sequence.get_len()
sequence.get_sequence()



p = PerlWrapper( 'DDB::PROTEIN')




















class Foo(object):
    def __getattribute__(self,name):
        attr = object.__getattribute__(self, name)
        if hasattr(attr, '__call__'):
            def newfunc(*args, **kwargs):
                print('before calling %s' %attr.__name__)
                attr(*args, **kwargs)
                print('done calling %s' %attr.__name__)
            return newfunc
        else:
            print('Retrieve attribute %s' % name)
            return attr


class Bar(Foo):
    def myFunc(self, data):
        self.test = 42
        print("myFunc: %s"% data)

bar = Bar()
bar.myFunc(5)
bar.test



