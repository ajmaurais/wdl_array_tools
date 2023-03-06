
import os
import sys
from hashlib import md5

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), './data'))

def md5_sum(fname):
    ''' Get the md5 digest of a file. '''
    file_hash = md5()
    with open(fname, 'rb') as inF:
        while chunk := inF.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import src

