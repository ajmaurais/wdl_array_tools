
import argparse
import sys
from os.path import basename
import re
import json
from typing import List, Set

def arrays_overlap(arrays: List[Set]) -> Set:
    overlap = set()
    for rhs in arrays:
        for lhs in arrays:
            if rhs is lhs:
                continue
            overlap = overlap.union(rhs & lhs)
    return overlap


class Main(object):
    '''
    A class to parse subcommands.
    Inspired by this blog post: https://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html
    '''

    ARRAYS_OVERLAP_DESCRIPTION = 'Exit with non return code of 1 if any elements in input arrays are the same.'

    def __init__(self):
        parser = argparse.ArgumentParser(description='Helpful array opperations for use in wdl workflows.',
                                         usage = f'''wdl_arrray_tools <command> [<args>]

Available commands:
   arrays_overlap       {Main.ARRAYS_OVERLAP_DESCRIPTION}''')
        parser.add_argument('command', help = 'Subcommand to run.')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            sys.stderr.write(f'{args.command} is an unknown command!')
            parser.print_help()
            sys.exit(1)
        getattr(self, args.command)()


    def arrays_overlap(self):
        parser = argparse.ArgumentParser(description=Main.ARRAYS_OVERLAP_DESCRIPTION)
        parser.add_argument('--sep', default=r'\s*,\s*',
                            help='A RegEx to separate elements in input arrays. Default is "\s*,\s*"')
        parser.add_argument('--use_basename', default = False, action='store_true',
                            help='Use file basename of array elements? Default is false.')
        parser.add_argument('-a', '--add_array', action='append', default=None,
                            help='Add array formated as string with elements seperated by commas')
        parser.add_argument('-i', '--input_json', default=None,
                            help='Give input arrays serialized in json file.')
        args = parser.parse_args(sys.argv[2:])

        arrays = list()
        if args.input_json:
            with open(args.input_json, 'r') as inF:
                arrays = json.load(inF)

            # validate input
            if not all(isinstance(l, list) for l in arrays) or not all(isinstance(v, str) for l in arrays for v in l):
                sys.stderr.write('Invalid format for input_json!\n')
                sys.exit(1)

            arrays = [set(x) for x in arrays]

        elif args.add_array:
            split_re = re.compile(args.sep)
            arrays += [set(split_re.split(s.strip())) for s in args.add_array]

        if args.use_basename:
            for i in range(len(arrays)):
                arrays[i] = {basename(x) for x in arrays[i]}
        
        if overlap := arrays_overlap(arrays):
            sys.stderr.write(f'Overlapping elements found in arrays:\n{overlap}\n')
            sys.exit(1)


def main():
    _ = Main()


if __name__ == '__main__':
    main()

