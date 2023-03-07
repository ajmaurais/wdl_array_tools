
import unittest
import os
import tempfile
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from context import md5_sum, src, DATA_DIR
from src.submodules.Tsv import Tsv


class TestTsv(unittest.TestCase):

    PROTEIN_TSV = f'{DATA_DIR}/2_reps/protein_abundance_long.tsv'
    PROTEIN_ANNOTATIONS = f'{DATA_DIR}/2_reps/replicate_annotations.csv'
    PROTEIN_ARGS = ('ReplicateName', 'ReplicateLocator', 'ProteinAbundance')
 
    def test_can_read_tsv(self):
        tsv = Tsv()
        self.assertTrue(tsv.read(TestTsv.PROTEIN_TSV, *TestTsv.PROTEIN_ARGS))

    def test_name_to_locator(self):
        for _ in range(100):
            tsv = Tsv()
            self.assertTrue(tsv.read(TestTsv.PROTEIN_TSV, *TestTsv.PROTEIN_ARGS))
            key_value_pairs = [(v.replace('Replicate:/', ''), k) for k, v in tsv.name_to_locator.items()]
            for lhs, rhs in key_value_pairs:
                self.assertEqual(lhs, rhs)

    def test_is_deterministic_2_reps(self):
        md5s = set()
        with tempfile.TemporaryDirectory() as tmp:
            for i in range(50):
                tsv = Tsv()
                self.assertTrue(tsv.read(TestTsv.PROTEIN_TSV, *TestTsv.PROTEIN_ARGS))
                tsv.read_annotations(TestTsv.PROTEIN_ANNOTATIONS)
                fname = os.path.join(tmp, f'out_{i}.gct')
                tsv.write_gct(fname)
                md5s.add(md5_sum(fname))
        self.assertTrue(len(md5s) == 1)

    def test_is_deterministic_4_reps(self):
        protein_tsv = f'{DATA_DIR}/4_reps/subset.tsv'
        protein_annotations = f'{DATA_DIR}/4_reps/replicate_annotations.csv'
        md5s = set()
        with tempfile.TemporaryDirectory() as tmp:
            for i in range(50):
                tsv = Tsv()
                self.assertTrue(tsv.read(protein_tsv, 'Replicate Name', 'Replicate Locator', 'Protein Abundance'))
                tsv.read_annotations(protein_annotations)
                fname = os.path.join(tmp, f'out_{i}.gct')
                tsv.write_gct(fname)
                md5s.add(md5_sum(fname))
        self.assertTrue(len(md5s) == 1)

    def test_get_expected_result_4_reps(self):
        protein_tsv = f'{DATA_DIR}/4_reps/subset.tsv'
        protein_annotations = f'{DATA_DIR}/4_reps/replicate_annotations.csv'
        target_md5 = md5_sum(f'{DATA_DIR}/4_reps/subset.gct')
        md5s = set()
        with tempfile.TemporaryDirectory() as tmp:
            for i in range(50):
                tsv = Tsv()
                self.assertTrue(tsv.read(protein_tsv, 'Replicate Name', 'Replicate Locator', 'Protein Abundance'))
                tsv.set_id_cols(['Protein'])
                tsv.read_annotations(protein_annotations)
                fname = os.path.join(tmp, f'out_{i}.gct')
                tsv.write_gct(fname)
                self.assertTrue(md5_sum(fname) == target_md5)

    def test_get_expected_result_2_reps(self):
        target_md5 = md5_sum(f'{DATA_DIR}/2_reps/protein_abundance_long.gct')
        md5s = set()
        with tempfile.TemporaryDirectory() as tmp:
            for i in range(50):
                tsv = Tsv()
                self.assertTrue(tsv.read(TestTsv.PROTEIN_TSV, *TestTsv.PROTEIN_ARGS))
                tsv.set_id_cols(['Protein'])
                tsv.read_annotations(TestTsv.PROTEIN_ANNOTATIONS)
                fname = os.path.join(tmp, f'out_{i}.gct')
                tsv.write_gct(fname)
                self.assertTrue(md5_sum(fname) == target_md5)

if __name__ == '__main__':
    unittest.main(verbosity=2)

