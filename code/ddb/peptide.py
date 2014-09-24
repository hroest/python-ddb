import ddb
from ddb.shared import *

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
        '_pi' : [0.0,'read/write'],
        '_molecular_weight' : [0.0,'read/write'],
        '_file_key' : [0,'read/write']
     }

    def __init__(self, **kwargs):
        perl.require( 'DDB::PEPTIDE' )
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

    def get_proteins(self, load=False):
        proteins = [ddb.Protein(id = p_id) for p_id in self.get_protein_ids() ]
        for pr in proteins:
            if load:
                pr.load()

        return proteins

    @staticmethod
    def find_by_sequence_and_experiment_key(sequence, experiment_key):
        db = config.get_db_connector()
        #cursor = config.get_db_cursor()
        cursor = db.cursor()
        cursor.execute( 'SELECT id from ' + Peptide.__table__ + 
                       ' where sequence = %s and experiment_key = %s', 
                      ( sequence, experiment_key)  )
        #due to mysql constraints, there is only one result
        return Peptide( id = cursor.fetchall()[0][0] )

