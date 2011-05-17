import MySQLdb
from sqlalchemy import MetaData, create_engine, Table

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


protein_table = Table('protein', mymetadata,autoload=True)
peptide_table = Table('peptide', mymetadata,autoload=True)
gene_table =    Table('gene', mymetadata,autoload=True)
protPepLink_table = Table('protPepLink', mymetadata, autoload=True)
geneProtLink_table = Table('geneProtLink', mymetadata,autoload=True)
feature_table = Table('feature', metadata_genome,autoload=True)
sequence_table = Table('sequence', metadata_meta,autoload=True)
