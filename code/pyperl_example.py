import ddb

###################################
## Explore the generic PerlWrapper
###################################
mygene = ddb.PerlWrapper('DDB::GENE')
mygene.set_id(1)
mygene.load()
print "Loaded Gene 1:"
print mygene.get_ensembl_stable_id()
print mygene.get_description()
print mygene.get_experiment_key()

mypeptide = ddb.PerlWrapper('DDB::PEPTIDE')
mypeptide.set_id(1)
mypeptide.load()
print "\nLoaded Peptide 1:"
print mypeptide.get_pi()
print mypeptide.get_experiment_key()

###################################
## Explore the specific implementations of objects that we already have
###################################
print "\n###################################\nUse specific object wrappers: \n"
print "Protein level (get Protein 1):"
p = ddb.Protein()
p.set_id(1)
p.load()
print p.get_sequence_key()
print p.exists()

print "\nPeptide level (get Peptide 1):"
pep = ddb.Peptide()
pep.set_id(1)
pep.load()

print pep.get_molecular_weight()
print pep.get_pi()
print pep.get_experiment_key()
print pep.get_parent_sequence_key()
print pep.get_peptide_type()
# Iterate through all proteins
print ("Iterate through all proteins assocated with this peptide:")
for pr in pep.get_proteins(True):
    print ("  - We have a protein here with id %s and experiment_key %s and sequence_key %s." % (
        pr.get_id(), pr.get_experiment_key(), pr.get_sequence_key()) )


