# tutorial
from sqlalchemy.orm import sessionmaker

from db_tables import *
from objects import *

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

