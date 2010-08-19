from ddb.shared import *

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
        perl.require( 'DDB::SEQUENCE' )
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
