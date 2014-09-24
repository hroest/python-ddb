import ddb
print "Protein level:"
p = ddb.Protein()
p.set_id(1)
p.load(_id=1)
p.exists()
print "Peptide level:"
pep = ddb.Peptide()
pep.set_id(1)
pep.load(_id=1)
pep.get_proteins()
pep.get_molecular_weight()
pep.get_pi()
pep.get_experiment_key()
pep.get_parent_sequence_key()
pep.get_peptide_type()

