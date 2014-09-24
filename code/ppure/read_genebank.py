# tutorial
from db_tables import *
from objects import *

import sys
from Bio import SeqIO, Seq
import Bio.Data.CodonTable

file = sys.argv[1]
fasta_file = file
records = list(SeqIO.parse(open(fasta_file,"r"), "fasta"))
assert len(records) == 1
desc = records[0].description.split('|')[-1].strip()
ref = records[0].description.split('|')[-2].strip()
gid = records[0].id.split('|')[1].strip()
fasta_sequence = records[0].seq
print desc, ref, gid

# DDB objects:
# - add an experiment
# - add a genome sequence
# - add a genome

exp = Experiment(super_experiment_key = 3805, name = desc, short_description = ref)
exp = exp.addignore_setid(session)

gseq = GenomeSeq(sequence = fasta_sequence)
gseq.addignore_setid(session)
genome_id = gseq.id

genome = Genome(experiment_key = exp.id, id=genome_id, gi=gid, 
                ref=ref, description=desc, comment='')
genome.addignore_setid(session) 

gb_file = file.split('.')[0]+'.gb'
records = list(SeqIO.parse(open(gb_file,"r"), "genbank"))
assert len(records) == 1
i = 0
for gb_record in records[0].features:
    i += 1
    # now do something with the record
    pseudo = 'no'
    if gb_record.qualifiers.has_key('pseudo'): pseudo = 'yes'
    start = gb_record.location.start.position
    end = gb_record.location.end.position
    strand = '+'
    if gb_record.strand == -1: strand = '-'
    db_xref='';gene='';locus_tag='';note='';codon_start='';transl_table='';product='';protein_id='';ec_number='';gene_synonym='';function=''
    f = gb_record
    if f.qualifiers.has_key('db_xref'     ):   db_xref =      str(f.qualifiers['db_xref'][0]) 
    if f.qualifiers.has_key('gene'        ):   gene=          f.qualifiers['gene'][0]
    if f.qualifiers.has_key('locus_tag'   ):   locus_tag =    f.qualifiers['locus_tag'][0]
    if f.qualifiers.has_key('note'        ):   note =         f.qualifiers['note'][0]
    if f.qualifiers.has_key('codon_start' ):   codon_start =  f.qualifiers['codon_start'][0]
    if f.qualifiers.has_key('transl_table'):   transl_table = f.qualifiers['transl_table'][0]
    if f.qualifiers.has_key('product'     ):   product =      f.qualifiers['product'][0]
    if f.qualifiers.has_key('protein_id'  ):   protein_id =   f.qualifiers['protein_id'][0]
    if f.qualifiers.has_key('ec_number'   ):   ec_number =    f.qualifiers['ec_number'][0]
    if f.qualifiers.has_key('gene_synonym'):   gene_synonym = f.qualifiers['gene_synonym'][0]
    if f.qualifiers.has_key('function'    ):   function =     f.qualifiers['function'][0]

    if f.type != 'source':
        #we translate it and find the sequence key 
        sequence = fasta_sequence[ start : end ]
        if f.strand == -1: sequence = sequence.reverse_complement()
        #cds means wheter we enforce a start and a stop codon here
        cds = False; 
        if f.type == 'CDS': cds = True
        try:
            if transl_table is None: translated = sequence.translate(table=11, cds=cds,to_stop=True).tostring()
            else: translated = sequence.translate(table=11, cds=cds, to_stop=True).tostring()
            ddbseq = Sequence(sequence = translated)
            ddbseq = ddbseq.addignore_setid(session)
            sequence_key = ddbseq.id
        except Bio.Data.CodonTable.TranslationError: 
            if pseudo == 'no' and product.find('pseudogene') == -1: print 'not translated'; print sequence; print pseudo; print f;
            sequence_key = 0
    else: sequence_key = 0

    # Hack to be sure to have unique misc_feature
    if f.type == 'misc_feature': ftype = "misc_feature_%s" % i
    else: ftype = f.type

    feature = Feature(genome_key = genome_id, sequence_key = sequence_key, 
                  start = start, end = end, strand = strand, type = ftype,
                  db_xref      =   db_xref,
                  gene         =   gene,
                  locus_tag    =   locus_tag ,
                  note         =   note ,
                  codon_start  =   codon_start ,
                  transl_table =   transl_table ,
                  product      =   product ,
                  protein_id   =   protein_id ,
                  ec_number    =   ec_number ,
                  gene_synonym =   gene_synonym ,
                  function     =   function ,
                  pseudo       = pseudo,
                  mol_type='genomic DNA')
    session.add(feature)
    
session.commit()

# cursor.execute( "insert into ddbGenome.genomeSeq (compress_seq) VALUES (compress('%s')) " % fasta_sequence )
# genome_id = mydb.insert_id()
# print "insert" , genome_id
# 

#session.add(genome)
#session.commit()
