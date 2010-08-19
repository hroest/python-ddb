import random
import unittest

import sys
sys.path.append( './')
import ddb

testexperiment = 3331
testprotein = 3174147
testsequence = 18075093
testpeptide = 11861373

class TestProtein(unittest.TestCase):
    "Test Protein class"

    def setUp(self):
        self.protein = ddb.Protein()

    def test_addignore_protein(self):
        p = self.protein
        p.set_sequence_key( testsequence )
        p.set_experiment_key( testexperiment )
        p.set_parse_key( 1 )
        p.set_probability( 0.6 )
        p.addignore_setid()

    def test_get_protein(self):
        self.test_addignore_protein()
        p = self.protein
        self.assertEqual( int( p.id ), testprotein )
        self.assertEqual( p.id, p._id)
        self.assertEqual( p.id, p.get_id())
        self.assertEqual( p.id, p.ref['_id'])

    def test_set_protein(self):
        self.test_addignore_protein()
        p = self.protein
        p.id = 20
        self.assertEqual(int(p.ref['_id']), 20)
        p._id = 21
        self.assertEqual(int(p.ref['_id']), 21)
        p.set_id(22)
        self.assertEqual(int(p.ref['_id']), 22)
        p.ref['_id'] = 23
        self.assertEqual(int(p.ref['_id']), 23)

    def test_sequence_protein(self):
        self.test_addignore_protein()
        p = self.protein
        s = p.get_sequence()
        self.assertEqual( s.get_sequence(), 'PROTEIN')
        self.assertEqual( int( s.get_position( s.get_sequence() ) ), 1)

    def test_missing_sequence_protein(self):
        p = self.protein
        try:
            s = p.get_sequence()
        except ddb.AttributeMissingError: pass
        else: self.fail('Should not access sequence if its not there')

class TestDDBAbstraction(unittest.TestCase):
    "General ddb abstraction test with read-only attributes"

    def setUp(self):
        self.test = ddb.ddbTestObject()

    def test_read_only_attributes(self):
        test=self.test
        test.get_test_readonly()
        try:
            test.set_test_readonly()
        except Exception:pass
        else: self.fail("should not set read only attribute")
        test.test_readonly
        try:
            test.test_readonly = 8
        except ddb.AccessError: pass
        else: self.fail("should not set read only attribute")

class TestSequence(unittest.TestCase):
    "Test Sequence class"

    def setUp(self):
        self.sequence = ddb.Sequence()

    def test_addignore_sequence(self):
        s = self.sequence
        s.db = 'testdb'
        s.ac = 'test'
        s.ac2 = 'test'
        s.description = 'testsequence'
        s.sequence = 'PROTEIN'
        s.addignore_setid()

    def test_get_sequence(self):
        self.test_addignore_sequence()
        s = self.sequence
        self.assertEqual( int( s.id ), testsequence )
        self.assertEqual( s.id, int(s._id) )
        self.assertEqual( s.id, s.get_id())
        self.assertEqual( s.id, int(s.ref['_id']) )

class TestPeptide(unittest.TestCase):
    "Test Peptide class"

    def setUp(self):
        self.peptide = ddb.Peptide()

    def test_addignore_sequence(self):
        p = self.peptide
        p.peptide = 'PEPTIDE'
        p.experiment_key = testexperiment
        p.peptide_type = 'bioinfo'
        p.addignore_setid()
        self.assertEqual( testpeptide, p.id )

    def test_creation_method(self):
        p = ddb.Peptide(peptide='PEPTIDE',experiment_key=testexperiment,peptide_type='bioinfo')
        p.addignore_setid()
        self.assertEqual( testpeptide, p.id )


unittest.main()
