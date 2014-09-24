
import sys
sys.path.append('./pyDDB')
import objects
from db_tables import session, connection_creator
from Bio import SeqIO, Seq
import Bio.Data.CodonTable

ExperimentKey = 4122

# Retrieve a genome from ddb.genome by its experiment key
current_genome = session.query(objects.Genome).filter_by(experiment_key=ExperimentKey).first()
print("Found genome %s (%s) which is annotated as %s." % (current_genome.id, current_genome.ref, current_genome.description))

# Select some features found in that genome
features = [f for f in current_genome.features if f.type == "CDS"] 
print("This genome has %s CDS features." % ( len(features)))

# Select some features with at least one SNP
mga_feature = [f for f in features if f.gene == "mga"][0]
print("Found gene %s with sequence id %s" % ( mga_feature, mga_feature.sequence_key ))

# Check how many SNPs this feature has
print("Gene %s has %s annotated SNPs." % ( mga_feature.gene, len(mga_feature.snps) ))
for snp in mga_feature.snps:
    aamut = mga_feature.map_mutation(snp)
    print("SNP %s found at position %s is a mutation from %s to %s -> %s" %(snp.id, snp.position, snp.original_char, snp.mutated_char, str(aamut)) )

