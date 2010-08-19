import perl
perl.eval( "use lib './' ")
perl.require( 'DDB::GENE' )
perl.require( 'DDB::PROTEIN' )
perl.require( 'DDB::SEQUENCE' )
perl.require( 'DDB::PEPTIDE' )



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



