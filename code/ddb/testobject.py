from ddb.shared import *

perl.require( 'DDB::PROTEIN' )
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
        print('here in Python get x')
        return self._x 
    def setx(self, val):
        print('here in Python set x')
        self._x = val
    x = property(getx, setx)
