
import sys
import os
import argparse

from .submodules.Tsv import Tsv

def main():
    parser = argparse.ArgumentParser(description='Convert easy to use long formated .tsv files into the difficult to use gct format.')
    parser.add_argument('--namesFrom', default='ReplicateName',
                        help='Column to get column names from.')
    parser.add_argument('--namePathFrom', default='ReplicateLocator',
                        help='The element locator that links elements to the annotation file.')
    parser.add_argument('--valuesFrom', default='ProteinAbundance',
                        help='Column to get values from.')
    parser.add_argument('tsv', help='Long formated .tsv file')
    parser.add_argument('annotations', help='Annotations file corresponding to `tsv`.')
    args = parser.parse_args()

    tsv = Tsv()
    tsv.read(args.tsv, args.namesFrom, args.namePathFrom, args.valuesFrom)
    tsv.read_annotations(args.annotations)

    ofname = os.path.splitext(os.path.basename(args.tsv))[0] + '.gct'
    tsv.write_gct(ofname)


if __name__ == '__main__':
    main()

