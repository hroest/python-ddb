import perl
from ddb.shared import PerlWrapper
perl.eval( "use lib './' ")
perl.require( 'DDB::GENE' )
perl.require( 'DDB::PROTEIN' )
perl.require( 'DDB::SEQUENCE' )
perl.require( 'DDB::PEPTIDE' )

myobj = PerlWrapper('DDB::GENE')
myobj.ref[ '_ensembl_stable_id' ] 
myobj.get_ensembl_stable_id()
myobj._ensembl_stable_id 
#myobj.ensembl_stable_id  #this doesnt work
myobj.set_ensembl_stable_id(9)
myobj._ensembl_stable_id = 42
myobj.get_ensembl_stable_id()







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

import ddb
p = ddb.Protein()
pep = ddb.Peptide()
seq = ddb.Sequence()


