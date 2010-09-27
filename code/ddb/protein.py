from ddb.shared import *

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

    def __init__(self, **kwargs):
        perl.require( 'DDB::PROTEIN' )
        PerlWrapper.__init__( self, 'DDB::PROTEIN')
        for attr in Protein._attr_data:
            #self.__dict__[ attr ] = _attr_data[attr][0]
            #exec("self.%s = Protein._attr_data['%s'][0]" % (attr, attr) ) 
            setattr( self, attr, self.__class__._attr_data[attr][0] )
            pass
        self._sequence_loaded = False
        for k in kwargs:
            if '_' + k in self.__class__._attr_data.keys(): 
                if debug: print(k + ' is in _attr_data')
                setattr(self, '_' + k, kwargs[k] )
            if debug: print(k)

    def _load_sequence(self):
        from ddb.sequence import Sequence
        if not self.sequence_key: 
            raise AttributeMissingError('sequence_key')
        self._sequence = Sequence(id=self.sequence_key)
        self._sequence.load()
        self._sequence_loaded = True

    def get_sequence(self):
        if not self._sequence_loaded: self._load_sequence()
        return self._sequence
