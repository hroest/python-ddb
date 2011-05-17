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
#declarative
from sqlalchemy.ext.declarative import declarative_base
def connect():
    return MySQLdb.connect( read_default_file='~/.my.cnf')

db = create_engine('mysql://', creator=connect)
db.echo = False  
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

#querying
mypeptide = session.query(Peptide).filter_by(id='11861373').first() 

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




