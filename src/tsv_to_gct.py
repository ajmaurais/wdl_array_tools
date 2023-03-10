
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
    parser.add_argument('--idCols', default=None,
                        help='The columns to get row ids from. '
                             'Should be a string with column names seperated by commas.')
    parser.add_argument('--idSep', default='_', help='The seperator in case of multiple idCols.')
    parser.add_argument('--debug', default=None, choices=['pudb', 'pdb'],
                        help='Start main method in selected debugger.')
    parser.add_argument('tsv', help='Long formated .tsv file')
    parser.add_argument('annotations', help='Annotations file corresponding to `tsv`.')
    args = parser.parse_args()

    if args.debug == 'pudb':
        import pudb as debugger
        debugger.set_trace()
    elif args.debug == 'pdb':
        print('What is wrong with you?\nYou should be using pudb you jack rabbit!')
        sys.exit(1)

    tsv = Tsv()
    tsv.read(args.tsv, args.namesFrom, args.namePathFrom, args.valuesFrom)
    tsv.read_annotations(args.annotations)

    if args.idCols:
        tsv.set_id_cols([x.strip() for x in args.idCols.split(',')])

    ofname = os.path.splitext(os.path.basename(args.tsv))[0] + '.gct'
    tsv.write_gct(ofname, id_sep=args.idSep)


if __name__ == '__main__':
    main()

