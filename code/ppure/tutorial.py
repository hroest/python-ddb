# tutorial
# http://www.sqlalchemy.org/docs/05/ormtutorial.html
# please read for connecting tables, foreign keys etc
# it is most fun to do this in an interactive shell and 
# do it step for step. Then you can see the difference in the
# mysql table with each step!
# just running it is not so much fun because it undoes all the changes!
import MySQLdb
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.databases.mysql import MSEnum
from sqlalchemy.types import Binary
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relation, backref
#declarative
from sqlalchemy.ext.declarative import declarative_base

def connection_creator(db):
    #this fxn will return a fxn "connect" which returns a database connector
    def connect():
        return MySQLdb.connect( read_default_file='~/.my.cnf', db=db)
    return connect

db = create_engine('mysql://', creator=connection_creator('ddb'), echo = False)
db.echo = False  
db_genome = create_engine('mysql://', creator=connection_creator('ddbGenome'), echo = False)
db_genome.echo = False  

Base = declarative_base()
class Peptide(Base):
    __tablename__ = 'peptide'
    #
    id = Column('id', Integer, primary_key=True)
    experiment_key = Column('experiment_key', Integer)
    peptide_type = Column('peptide_type', String)
    sequence = Column('sequence', String)
    parent_sequence_key = Column('parent_sequence_key', Integer)
    molecular_weight = Column('molecular_weight', Float)
    pi = Column('pi', Float)
    #
    def __init__(self, experiment_key, peptide_type, sequence, parent_sequence_key, molecular_weight, pi):
        self.experiment_key = experiment_key
        self.peptide_type = peptide_type
        self.sequence = sequence
        self.parent_sequence_key = parent_sequence_key
        self.molecular_weight = molecular_weight
        self.pi = pi
    #
    def __repr__(self):
       return "<Peptide('%s','%s')>" % (self.experiment_key, self.sequence )

Session = sessionmaker(bind=db)
session = Session()

GenomeBase = declarative_base()
class Genome(GenomeBase):
    __tablename__ = 'genome'
    #
    id             = Column('id',             Integer, primary_key=True)
    experiment_key = Column('experiment_key', Integer)
    gi             = Column('gi',             Integer)
    ref            = Column('ref',            String)
    description    = Column('description',    String)
    comment        = Column('comment',        String)
    insert_date    = Column('insert_date',    Date)
    timestamp      = Column('timestamp',      TIMESTAMP)
    #
    #features = relation('Feature', order_by='Feature.id', backref="feature")
    #
    def __init__(self, **kwargs): 
        # we go through all arguments given as keywords and set them 
        # e.g. if init was called with (id=someid) we set here self.id = someid
        for k in kwargs:
            setattr( self, k, kwargs[k])
    def __repr__(self):
       return "<Genome('%s',id '%s', '%s')>" % (self.experiment_key, self.id, self.description )

class Feature(GenomeBase):
    __tablename__ = 'feature'
    #
    id           = Column('id',             Integer, primary_key=True)
    genome_key   = Column('genome_key', Integer , ForeignKey('genome.id') )
    sequence_key = Column('sequence_key',             Integer)
    start        = Column('start',             Integer)
    end          = Column('end',             Integer)
    strand       = Column('strand',             Integer)
    type         = Column('type',             String)
    pseudo       = Column('pseudo',            MSEnum('yes','no') )
    mol_type     = Column('mol_type',    String)
    db_xref      = Column('db_xref',        String)
    gene         = Column('gene',        String)
    locus_tag    = Column('locus_tag',        String)
    note         = Column('note',        String)
    codon_start  = Column('codon_start',        String)
    transl_table = Column('transl_table',        String)
    product      = Column('product',        String)
    protein_id   = Column('protein_id',        String)
    ec_number    = Column('ec_number',        String)
    gene_synonym = Column('gene_synonym',        String)
    function     = Column('function',        String)
    pan          = Column('pan',         MSEnum('yes','no') )
    insert_data  = Column('insert_date',    Date)
    timestamp    = Column('timestamp',      TIMESTAMP)
    #
    genome = relation('Genome', order_by='Genome.id', backref=backref("features", order_by=id)) 
    #
    def __init__(self, **kwargs): 
        # we go through all arguments given as keywords and set them 
        # e.g. if init was called with (id=someid) we set here self.id = someid
        for k in kwargs:
            setattr( self, k, kwargs[k])
    def __repr__(self):
       return "<Feature(seq '%s', genome '%s', '%s', '%s', '%s')>" % (self.genome_key, self.sequence_key, self.start, self.end, self.gene )



class GenomeSeq(GenomeBase):
    __tablename__ = 'genomeSeq'
    #
    id           = Column('id',  Integer, ForeignKey('genome.id'), primary_key=True, )
    compress_seq = Column('compress_seq', Binary)
    #
    genome = relation('Genome', order_by='Genome.id', backref=backref("genomeSeq", uselist=False)) 
    #
    def __init__(self, **kwargs): 
        # we go through all arguments given as keywords and set them 
        # e.g. if init was called with (id=someid) we set here self.id = someid
        for k in kwargs:
            setattr( self, k, kwargs[k])
    def __repr__(self):
       return "<Genome Sequence(id '%s')>" % (self.id)




genomeSession = sessionmaker(bind=db_genome)
genomesession = genomeSession()

#querying
mypeptide = session.query(Peptide).filter_by(id='11861373').first() 
mygenome = genomesession.query(Genome).filter_by(id='1').first() 
myfeature = genomesession.query(Feature).filter_by(id='1').first() 
mygseq = genomesession.query(GenomeSeq).filter_by(id='1').first() 

print myfeature
print myfeature.genome
print 'len', len(myfeature.genome.features)
print mygseq 
print mygseq.genome
print mygseq.genome.genomeSeq


#creating
other_peptide = Peptide(3331, 'test', 'PEPTIDEE', 0, 0, 0)
session.add(other_peptide)

#we havent committed yet, our session knows that
session.dirty
session.new

session.commit()


#update
other_peptide = session.query(Peptide).filter_by(sequence='PEPTIDEE').first() 
other_peptide.sequence = 'SOMECRAZYPEPTIDE'
session.commit()

#update (restore it to what it was)
other_peptide = session.query(Peptide).filter_by(sequence='SOMECRAZYPEPTIDE').first() 
other_peptide.sequence = 'PEPTIDEE'
session.commit()


#deleting
other_peptide = session.query(Peptide).filter_by(sequence='PEPTIDEE').first() 
session.delete(other_peptide)
session.commit()





#more advanced stuff of filtering and selecting
#get all sequences with exp_key 3331
for sequence in session.query(Peptide).filter(Peptide.experiment_key=='3331'): 
    print sequence

#nearly SQL
for sequence in session.query(Peptide).filter('experiment_key=3331'): 
    print sequence

#real SQL
for pep in session.query(Peptide).from_statement('SELECT * FROM peptide where experiment_key=3331'):
    print pep




