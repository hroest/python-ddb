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
mymetadata = MetaData(); mymetadata.bind = db
db_genome = create_engine('mysql://', creator=connection_creator('ddbGenome'), echo = False)
metadata_genome = MetaData(); metadata_genome.bind = db_genome
db_meta = create_engine('mysql://', creator=connection_creator('ddbMeta'), echo = False)
metadata_meta = MetaData(); metadata_meta.bind = db_meta


Base_meta = declarative_base()
Base_meta.metadata.bind = db_meta
Base_genome = declarative_base()
Base_genome.metadata.bind = db_genome


Base = declarative_base()
Base.metadata.bind = db

class ProtPepLink(Base): __tablename__ = 'protPepLink'; __table_args__ = {'autoload': True}
class GeneProtLink(Base): __tablename__ = 'geneProtLink'; __table_args__ = {'autoload': True}
class Sequence(object): pass
class Feature(object): pass

class Peptide(Base):
    __tablename__ = 'peptide'
    __table_args__ = {'autoload': True}
    def __repr__(self):
       return "<Peptide('%s','%s','%s')>" % (self.id, self.experiment_key, self.sequence )


print dir(Sequence)
print Sequence


from sqlalchemy import MetaData, create_engine, Table
from sqlalchemy.orm import sessionmaker, mapper, relation
feature_table = Table('feature', metadata_genome,autoload=True)
sequence_table = Table('sequence', metadata_meta,autoload=True)
mapper(Sequence, sequence_table)
mapper(Feature, feature_table , properties = {
    'sequence' : relation (Sequence, primaryjoin=
        feature_table.c.sequence_key==sequence_table.c.id, 
        foreign_keys=[feature_table.c.sequence_key]) }
      )

#Feature.sequence = relation ('Sequence', 
#        primaryjoin='Feature.sequence_key==Sequence.id', 
#        foreign_keys=['sequence_key', Sequence.id])

class Protein(Base):
    __tablename__ = 'protein'
    __table_args__ = {'autoload': True}
    peptides = relation('Peptide', secondary=ProtPepLink.__table__,
        primaryjoin='Protein.id==ProtPepLink.protein_key',
        secondaryjoin='ProtPepLink.peptide_key==Peptide.id',
        backref='proteins', 
        foreign_keys=['id', ProtPepLink.protein_key, ProtPepLink.peptide_key])
    sequence = relation ('Sequence', 
        primaryjoin='Protein.sequence_key==Sequence.id',
        backref='proteins',
        foreign_keys=[ProtPepLink.protein_key, ProtPepLink.peptide_key])

    def __repr__(self):
       return "<Protein('%s','%s','%s')>" % (self.id, self.experiment_key, 'asdf') #self.sequence )

# mapper(Protein, protein_table, properties = {
#     'peptides' : relation(Peptide, secondary=protPepLink_table,
#         primaryjoin=protein_table.c.id==protPepLink_table.c.protein_key, 
#         secondaryjoin=and_(protPepLink_table.c.peptide_key==peptide_table.c.id),
#         backref='proteins', 
#         foreign_keys=[protPepLink_table.c.protein_key, protPepLink_table.c.peptide_key]),
#     'genes' : relation(Gene, secondary=geneProtLink_table,
#         primaryjoin=protein_table.c.id==geneProtLink_table.c.protein_key, 
#         secondaryjoin=and_(geneProtLink_table.c.gene_key==gene_table.c.id),
#         backref='proteins', 
#         foreign_keys=[geneProtLink_table.c.protein_key, geneProtLink_table.c.gene_key])
# })



class Gene(Base):
    __tablename__ = 'gene'
    __table_args__ = {'autoload': True}
    def __repr__(self):
       return "<Gene('%s','%s','%s')>" % (self.id, self.experiment_key, self.description )


Session = sessionmaker()
session = Session()


myfeature = session.query(Feature).filter_by(id='1').first() 
print myfeature
print dir(myfeature)
print myfeature.sequence


mypeptide = session.query(Peptide).filter_by(experiment_key='3130').first() 
myprotein = session.query(Protein).filter_by(experiment_key='3130').first() 
print mypeptide
print myprotein
print myprotein.sequence
print myprotein.sequence.sha1
print myprotein.sequence.sequence
print myprotein.peptides
print '==================================='
print myprotein.peptides[5]
print len(myprotein.peptides[5].proteins)
print '==================================='
print myprotein.genes

import sys
sys.exit()

