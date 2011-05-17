from sqlalchemy.orm import mapper, relation
from sqlalchemy import and_
from tables import *

class Genome(object): pass

class Sequence(object): pass
mapper(Sequence, sequence_table)

class Feature(object): 
    def __repr__(self):
       return "<Feature(id '%s', seq '%s', genome '%s', '%s', '%s', '%s')>" % (self.id, self.genome_key, self.sequence_key, self.start, self.end, self.gene )

mapper(Feature, feature_table , properties = {
    'sequence' : relation (Sequence, primaryjoin=
        feature_table.c.sequence_key==sequence_table.c.id, 
        foreign_keys=[feature_table.c.sequence_key]) } )
 

class Peptide(object):
    def __repr__(self):
       return "<Peptide('%s','%s','%s')>" % (self.id, self.experiment_key, self.sequence )
mapper(Peptide, peptide_table)

class Gene(object):
    def __repr__(self):
       return "<Gene('%s','%s','%s')>" % (self.id, self.experiment_key, self.description )
mapper(Gene, gene_table)

class Protein(object):
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
        foreign_keys=[geneProtLink_table.c.protein_key, geneProtLink_table.c.gene_key])
})
