
import sys
import csv
from hashlib import md5


def detect_dialect(fname):
    with open(fname, 'r') as inF:
        dialect = csv.Sniffer().sniff(inF.readline(), delimiters=',\t')
    return dialect


class Tsv():
    def __init__(self):
        self.data = dict()
        self.headers = dict()
        self.name_to_locator = dict()
        self.annotations = dict()
        self._id_cols = None

    
    def set_id_cols(self, cols):
        id_cols = list()
        for col in cols:
            if col in self.headers:
                id_cols.append(self.headers[col])
            else:
                raise KeyError(f'{col} is an unknown column!')
        self._id_cols = tuple(id_cols)


    def read(self, fname: str, names_from: str, name_path_from: str, values_from: str):
        duplicates = dict()
        name_to_locator = set()
        with open(fname, 'r') as inF:
            reader = csv.reader(inF, dialect=detect_dialect(fname))

            # process header row
            headers = {cell: i for i, cell in enumerate(next(reader))}
            self.headers = {cell: i for cell, i in headers.items() if cell not in (names_from, values_from, name_path_from)}
            for col in [names_from, values_from, name_path_from]:
                if col not in headers:
                    raise RuntimeError(f'Missing required column "{col}" in {fname}')
            names_from_i = headers[names_from]
            values_from_i = headers[values_from]
            names_path_from_i = headers[name_path_from]

            for row in reader:
                keys = tuple(row[i] for i in self.headers.values())
                if keys not in self.data:
                    self.data[keys] = dict()

                # record duplicate keys (if any)
                if row[names_from_i] in self.data[keys]:
                    if keys not in duplicates:
                        duplicates[keys] = set()
                    duplicates[keys].add((row[names_from_i], row[values_from_i]))
                    duplicates[keys].add((row[names_from_i], self.data[keys][row[names_from_i]]))

                name_to_locator.add((row[names_path_from_i], row[names_from_i]))

                self.data[keys][row[names_from_i]] = row[values_from_i]
        
        # check that there wern't any duplicate elements recorded
        all_good = True
        if len(duplicates) > 0:
            sys.stderr.write(f'ERROR: There were {len(duplicates)} duplicate elements!\n')
            for duplicate in duplicates:
                sys.stderr.write(f'{duplicate}\n')
            all_good = False
        
        # populate self.name_to_locator
        for locator, name in name_to_locator:
            if name not in self.name_to_locator:
                self.name_to_locator[name] = locator
            else:
                if self.name_to_locator[name] != locator:
                    sys.stderr.write(f'Non unique name to locator mapping: {name} -> {locator}\n')
                    all_good = False
        
        return all_good


    def read_annotations(self, fname, locator_col='ElementLocator'):
        with open(fname, 'r') as inF:
            reader = csv.reader(inF, dialect=detect_dialect(fname))
            headers = {cell: i for i, cell in enumerate(next(reader))}
            if locator_col not in headers:
                raise RuntimeError(f'Missing required column "{locator_col}" in {fname}')
            self.annotation_cols = {k: i for k, i in headers.items() if k != locator_col}
            locator_col_i = headers[locator_col]

            for row in reader:
                if row[locator_col_i] not in self.annotations:
                    self.annotations[row[locator_col_i]] = dict()
                for annotation, index in self.annotation_cols.items():
                    self.annotations[row[locator_col_i]][annotation] = row[index]


    def _get_data_columns(self):
        replicates = set()
        for obs in self.data.values():
            for replicate in obs:
                replicates.add(replicate)
        return sorted(list(replicates))


    def _get_row_id(self, element, sep='_'):
        if self._id_cols is None:
            return md5('_'.join(element).encode('utf-8')).hexdigest()
        return sep.join([element[i] for i in self._id_cols])


    def write_gct(self, fname, id_sep='_'):
        
        data_cols = self._get_data_columns()
        key_col_NAs = '\t'.join(['NA'] * len(self.headers))
        
        with open(fname, 'w') as outF:
            outF.write('#1.3\n')
            outF.write(f'{len(self.data)}\t{len(data_cols)}\t{len(self.headers)}\t{len(self.annotation_cols)}\n')

            # print first column headers
            outF.write('\t'.join(['id'] + list(self.headers.keys()) + data_cols) + '\n')

            # print annotations
            for annotation in self.annotation_cols:
                outF.write(f'{annotation}\t{key_col_NAs}')
                for rep in data_cols:
                    outF.write('\t{}'.format(self.annotations[self.name_to_locator[rep]][annotation]))
                outF.write('\n')

            # print values
            for element, values in self.data.items():
                outF.write('{}\t'.format(self._get_row_id(element, sep=id_sep)))
                outF.write('\t'.join(element))
                for col in data_cols:
                    outF.write('\t{}'.format(values[col] if col in values else 'NA'))
                outF.write('\n')

