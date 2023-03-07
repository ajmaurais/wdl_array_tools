
import unittest
import os
import tempfile

from .context import md5_sum, src, DATA_DIR
from src.submodules.Tsv import Tsv


class TestTsv(unittest.TestCase):

    PROTEIN_TSV = f'{DATA_DIR}/protein_abundance_long.tsv'
    PROTEIN_ANNOTATIONS = f'{DATA_DIR}/replicate_annotations.csv'
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

    def test_is_deterministic(self):

        md5s = set()
        for i in range(50):
            tsv = Tsv()
            self.assertTrue(tsv.read(TestTsv.PROTEIN_TSV, *TestTsv.PROTEIN_ARGS))
            tsv.read_annotations(TestTsv.PROTEIN_ANNOTATIONS)
            # with tempfile.NamedTemporaryFile() as tmp:
            # with open(, 'r') as outF:
            fname = f'/home/ajm/code/wdl_array_tools/temp/out_{i}.gct'
            tsv.write_gct(fname)
            md5s.add(md5_sum(fname))
        self.assertTrue(len(md5s) == 1)
                    

if __name__ == '__main__':
    unittest.main(verbosity=2)

