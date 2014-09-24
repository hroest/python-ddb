from sqlalchemy.orm import mapper, relation, backref
from sqlalchemy import and_
from sqlalchemy import select
from db_tables import *
import datetime
from sqlalchemy import func #SQL functions like compress, sha1 etc
from sqlalchemy.orm import column_property

def add_init(myclass):
    """
    Allows the initialization of new database objects easily.

    This decorator adds a new __init__ function to the decorated class which
    can take one of two forms:
        - standard: through keywords
        - with defaults: through keywords and all fields are set to their default values

    For the second mechanism to work, the class needs to proivde a "_defaults"
    dictionary as a class member. For example, the following class:

    @add_init
    class Book(object): 

        _defaults = { 
            'ISBN'          : '978-3-16-148410-0',
            'url'           : 'http://www.example.com'
            'author'        : 'unknown',
            'title'         : '',
        }


    The added __init__ function has the signature __init__(self, **kwargs) and
    during initialization, setattr is used to try and set the value for each
    provided keyword argument.

    """

    def init_standard(self, **kwargs): 
        # we go through all arguments given as keywords and set them 
        # e.g. if init was called with (id=someid) we set here self.id = someid
        for k in kwargs:
            setattr( self, k, kwargs[k])

    def init_with_defaults(self, **kwargs): 
        for d in self.__class__._defaults:
            setattr( self, d, self.__class__._defaults[d])

        self.insert_date = datetime.datetime.utcnow().strftime('%Y-%m-%d')

        # we go through all arguments given as keywords and set them 
        # e.g. if init was called with (id=someid) we set here self.id = someid
        for k in kwargs:
            setattr( self, k, kwargs[k])

    # Select initialization method
    if myclass.__dict__.has_key('_defaults'):
        myclass.__init__ = init_with_defaults
    else:
        myclass.__init__ = init_standard

    return myclass

def add_addfxn(myclass):
    """
    Add a few default functions to a new class

    Adds the following functions (if they are not already present) to the wrapped object:
        - add (add and commit)
        - exists (check if current id already exists)
        - addignore_setid (add to table if current object does not yet exist)
    """

    #generic addignore
    def addignore_setid(self, session):
        p = self.exists(session)

        if p is None:
            return self.add(session)
        else:
            return p

    #generic exist, will only check whether this id is already present
    def exists(self, session):
        return session.query(self.__class__).filter_by(id=self.id).first()

    #generic add, will just use session
    def add(self, session):
        session.add(self)
        session.commit()
        return self

    if not myclass.__dict__.has_key('add'):
        myclass.add = add

    if not myclass.__dict__.has_key('exists'):
        myclass.exists = exists

    if not myclass.__dict__.has_key('addignore_setid'):
        myclass.addignore_setid = addignore_setid

    return myclass

def add_mapper(table):
    """
    Simple convenience class decorator

    Instead of writing

        class User(object):
            pass
        mapper(User, usertable)

    one can write directly

        @add_mapper(usertable)
        class User(object):
            pass

    which strenghtens the assocation between the object and its associated
    database.
    """

    def wrap(myclass):
        mapper(myclass, table)
        return myclass
    return wrap

@add_mapper(genome_table)
@add_addfxn
@add_init
class Genome(object): 

    _defaults = { 
        'gi'            : '',
        'ref'           : '',
        'description'   : '',
        'comment'       : '',
    }

@add_addfxn
@add_init
class GenomeSeq(object): 
    def get_sequence(self):
        return self._sequence
    def set_sequence(self, sequence):
        self._sequence = sequence
        self.compress_seq = func.compress(sequence)

    sequence = property(get_sequence,set_sequence)

mapper(GenomeSeq, genomeSeq_table, properties = {
    'id' : genomeSeq_table.c.id,
    'compress_seq' : genomeSeq_table.c.compress_seq,
    '_sequence' : column_property(func.uncompress(genomeSeq_table.c.compress_seq)),
})

@add_addfxn
@add_init
class Sequence(object): 

    def get_sequence(self):
        return self._sequence

    def set_sequence(self, sequence):
        self._sequence = sequence
        self.sha1 = func.sha1(func.upper(sequence))

    sequence = property(get_sequence,set_sequence)

    def exists(self, cursor): 
        return session.query(Sequence).filter_by(sha1=self.sha1).first()

    def __repr__(self):
        if self.sequence and len(self.sequence) > 80:
            rseq = self.sequence[:40] + '...' +  self.sequence[-40:]
        else: rseq = self.sequence
        return "<Sequence(id '%s', '%s', sequence '%s')>" % (self.id, self.sha1, rseq)

mapper(Sequence, sequence_table, properties = {
    '_sequence' : sequence_table.c.sequence,
    'id' : sequence_table.c.id,
    'sha1' : sequence_table.c.sha1,
})

@add_init
@add_addfxn
class Feature(object): 

    _defaults = { 
        'mol_type'      : '',
        'db_xref'       : '',   
        'gene'          : '',   
        'locus_tag'     : '',   
        'note'          : '',   
        'codon_start'   : '',   
        'transl_table'  : '',   
        'product'       : '',   
        'protein_id'    : '',   
        'ec_number'     : '',   
        'gene_synonym'  : '',   
        'function'      : '',   
    }

    def __repr__(self):
       return "<Feature(id '%s', genome '%s', seq '%s', '%s', '%s', '%s', '%s', '%s')>" % (self.id, self.genome_key, self.sequence_key, self.strand, self.type, self.start, self.end, self.gene )

mapper(Feature, feature_table , properties = {
    'sequence' : relation (Sequence, primaryjoin=
        feature_table.c.sequence_key==sequence_table.c.id, 
        foreign_keys=[feature_table.c.sequence_key]) } )
 
@add_mapper(peptide_table)
@add_addfxn
@add_init
class Peptide(object):
    def __repr__(self):
       return "<Peptide('%s','%s','%s')>" % (self.id, self.experiment_key, self.sequence )

    def exists(self, session):
        return session.query(self.__class__).filter_by(sequence=self.sequence, experiment_key=self.experiment_key).first()

@add_mapper(gene_table)
@add_addfxn
@add_init
class Gene(object):
    def __repr__(self):
       return "<Gene('%s','%s','%s')>" % (self.id, self.experiment_key, self.description )

@add_addfxn
@add_init
class Protein(object):

    def exists(self, session):
        return session.query(Protein).filter_by(experiment_key=self.experiment_key, sequence_key=self.sequence_key).first()

    def get_tryptic_peptides(self, min=5, max=60):
        start = 0
        for i,c in enumerate(self.sequence.sequence):
            prev = self.sequence.sequence[i-1]
            if i > 0 and c != 'P' and (prev == 'K' or prev == 'R'):
                pseq = self.sequence.sequence[start:i]
                start = i
                if len(pseq) < min or len(pseq) > max: continue
                pep = Peptide(experiment_key=self.experiment_key, sequence=pseq,
                    peptide_type='bioinformatics', parent_sequence_key = self.sequence.id, 
                    molecular_weight=-1, pi=-1)
                self.peptides.append( pep )

    def delete_peptides(self, session):
        for pep in self.peptides: session.delete(pep)
        session.commit()

    def __repr__(self):
       return "<Protein('%s','%s','%s')>" % (self.id, self.experiment_key, self.sequence )

mapper(Protein, protein_table, properties = {
    'sequence' : relation (Sequence, 
        primaryjoin=protein_table.c.sequence_key==sequence_table.c.id, 
        backref='proteins',
        foreign_keys=[protein_table.c.sequence_key]), 
    'peptides' : relation(Peptide, secondary=protPepLink_table,
        primaryjoin=protein_table.c.id==protPepLink_table.c.protein_key, 
        secondaryjoin=and_(protPepLink_table.c.peptide_key==peptide_table.c.id),
        backref='proteins', 
        foreign_keys=[protPepLink_table.c.protein_key, protPepLink_table.c.peptide_key]),
    'genes' : relation(Gene, secondary=geneProtLink_table,
        primaryjoin=protein_table.c.id==geneProtLink_table.c.protein_key, 
        secondaryjoin=and_(geneProtLink_table.c.gene_key==gene_table.c.id),
        backref='proteins', 
        foreign_keys=[geneProtLink_table.c.protein_key, geneProtLink_table.c.gene_key]),
    }, 
)


@add_addfxn
@add_init
class Experiment(object):

    _defaults = {
        'name'                   : '', 
        'short_description'      : '', 
        'description'            : '', 
        'super_experiment_key'   :  0, 
        'submitter'              : '', 
        'principal_investigator' : '', 
        'aim'                    : '', 
        'conclusion'             : '', 
        'experiment_type'        : 'bioinformatics', 
        'start_date'             : '0000-00-00', 
        'finish_date'            : '0000-00-00', 
        'public'                 : 'no', 
    }

    def __repr__(self):
       return "<Experiment('%s','%s','%s')>" % (self.id, self.name, self.short_description )

    def get_parents(self):
        p = self.parent
        l = [p]
        while p:
            p = p.parent
            if p: l.append(p)
        return l


mapper(Experiment, experiment_table, properties = {
    'proteins' : relation (Protein, 
        primaryjoin=protein_table.c.experiment_key==experiment_table.c.id, 
        backref=backref('experiment', uselist=False),
        foreign_keys=[protein_table.c.experiment_key]), 
    'parent' : relation (Experiment, 
        uselist=False,
        primaryjoin=experiment_table.c.super_experiment_key==experiment_table.c.id, 
        backref='children',
        foreign_keys=[experiment_table.c.super_experiment_key], 
        remote_side=[experiment_table.c.id]), 
    }, 
)
