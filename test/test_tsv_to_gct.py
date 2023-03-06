
import unittest
import os

from .context import src, DATA_DIR
from src.submodules.Tsv import Tsv


class TestTsv(unittest.TestCase):

    # path to test fasta file
    # TEST_FASTA = f'{DATA_DIR}/test.fasta'
    def test_generate_gct(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)

