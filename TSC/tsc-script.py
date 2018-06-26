"""
" The Shopping channel script
"
" Author: Michael Gorlin
"""
import os
import csv
import xlrd

from argparse import *

OUTPUT_NAMES = [
    'Item Number',
    'Category', 
    'Brand', 
    'Description', 
    'Quantity', 
    'Retail Price',
    'Ext. Retail Price', 
    'URL', 
    '6 Digit Item #',
    'Pallet ID'
]
QTY_INDEX = OUTPUT_NAMES.index('Quantity')
RET_INDEX = OUTPUT_NAMES.index('Retail Price')
EXT_INDEX = OUTPUT_NAMES.index('Ext. Retail Price')
CAT_INDEX = OUTPUT_NAMES.index('Category')

INPUT_NAMES = [
    ('Item Number', str),
    ('Category', str), 
    ('Brand Name', str),
    ('Description', str),
    ('Units On Hand', int),
    ('Original Price USD', float),
    ('Extended Retail Price USD', float),
    ('URL', str),
    ('6 digit item #', str),
    ('Pallet ID', str),
]

CAT_MAP = {
    'F' : 'Fashion',
    'C' : 'Cosmetics',
    'E' : 'Electronics',
    'J' : 'Jewellery',
    'H' : 'Home Goods'
}

_LOTS = {}

class Lot:
    """
    " This object stores the list of items in each lot. It maintains the 
    " expected retail and number of units and their actual values for 
    " verification purposes. When the lot is saved it sorts the rows
    " in descending expected retail order.
    """
    def __init__(self, lotnum, expunits, expret, outdir):
        global _LOTS
        self.lotnum = lotnum
        self.outfile = os.path.join(outdir, 'Lot %d.csv' % lotnum)
        self.expunits = expunits
        self.expret = expret
        self.values = []

        self.realret = 0.0
        self.realunits = 0

        self.loaded = False

        self._load()

    def _load(self):
        """
        " This loads a previously existing lot file.
        """
        self.values = [OUTPUT_NAMES]
        if os.path.exists(self.outfile):
            with open(self.outfile, 'r') as fin:
                reader = csv.reader(fin)
                next(reader)
                for row in reader:
                    row[EXT_INDEX] = float(row[EXT_INDEX])
                    row[RET_INDEX] = float(row[RET_INDEX])
                    row[QTY_INDEX] = int(row[QTY_INDEX])
                    
                    self.values.append(row)
                    self.realret += row[EXT_INDEX]
                    self.realunits += row[QTY_INDEX]
                self.loaded = True

    def add(self, value):
        qty = value[QTY_INDEX]
        ret = value[RET_INDEX]
        exr = value[EXT_INDEX]

        value[EXT_INDEX] = qty * ret
        value[CAT_INDEX] = CAT_MAP[value[CAT_INDEX]]

        if self.loaded:
            return

        self.realret += qty * ret
        self.realunits += qty
        self.values.append(value)
         
    def save(self):
        # Sort table by extended retail
        sfn = lambda val: float(val[EXT_INDEX])
        self.values[1:] = sorted(self.values[1:], key=sfn, reverse=True)

        # Round retail values
        for val in self.values[1:]:
            val[EXT_INDEX] = round(val[EXT_INDEX], 2)
            val[RET_INDEX] = round(val[RET_INDEX], 2)

        with open(self.outfile, 'w') as fout:
            writer = csv.writer(fout, dialect=csv.unix_dialect)
            writer.writerows(self.values)

    def verify(self):
        ostr = 'Verifying Lot %4d ----\n' % self.lotnum
        if self.realunits != self.expunits:
           ostr += '- failed quantity check '
           ostr += 'expected %d got %d\n' % (self.expunits, self.realunits)
        if self.realret != self.expret:
           ostr += '- failed expected retail check '
           ostr += 'expected $%.2f got $%.2f\n' % (self.expret, self.realret)
        print(ostr, flush=True)

def add_items(masterfile):
    wb = xlrd.open_workbook(masterfile)
    sh = wb.sheet_by_name('Manifest')

    headers = sh.row_values(0)

    try:
        indices = []
        lotindex = headers.index('Lot ID')
        for hname, _type in INPUT_NAMES:
            indices.append((headers.index(hname), _type))
    except ValueError as e:
        print(e)
        print(masterfile, 'is not formatted correctly.')
        exit()

    for i in range(1, sh.nrows):
        row = sh.row_values(i)
        lotv = row[lotindex]

        if lotv not in _LOTS:
            continue
    
        values = []
        for index, _type in indices:
            values.append(_type(row[index]))
        
        _LOTS[lotv].add(values)

def process_round(rfile, outdir):
    """
    " Here we create each lot object.
    " We extract the Lot number, Units, and Retail columns.
    """
    global _LOTS

    wb = xlrd.open_workbook(rfile)
    sh = wb.sheet_by_name('ROUND OVERVIEW')
    
    hrow = sh.row_values(0)

    try: 
        loti = hrow.index('LOT')
        uni  = hrow.index('Unit')
        reti = hrow.index('Retail (USD)')
    except ValueError:
        print(rfile, 'is not formatted correctly.', end='')
        return

    for i in range(1, sh.nrows):
        row = sh.row_values(i)

        lotv = int(row[loti])
        unv  = int(row[uni])
        retv = float(row[reti])

        if lotv in _LOTS.keys():
           continue  
        print('Adding Lot:', lotv, flush=True)

        _LOTS[lotv] = Lot(lotv, unv, retv, outdir)

    
def handle_rounds(rfiles, outdir):
    for rfile in rfiles:
        print('Processing - ', rfile, end='')

        if not os.path.exists(rfile):
            print(rfile, 'does not exist.', end='')
        elif os.path.splitext(rfile)[-1] != '.xlsx':
            print(rfile, 'is not a .xlsx file.', end='')
        else:
            process_round(rfile, outdir)
        print(flush=True)

if __name__ == '__main__':
    parser = ArgumentParser('The Shopping Channel script')
    parser.add_argument('-o', dest='outdir', help='Output Directory')
    parser.add_argument('master', help='Master Lot File')
    parser.add_argument('rounds', nargs='+', help='List of round files')
    
    args = parser.parse_args()

    outdir = '.'
    if args.outdir:
        outdir = args.outdir
        if not os.path.isdir(outdir):
            os.mkdir(outdir)
   
    if not os.path.exists(args.master):
        print('Master lot file does not exist.')
        exit()

    handle_rounds(args.rounds, outdir)

    add_items(args.master)

    for key in _LOTS:
        outlot = _LOTS[key]
        if outlot.verify():
            print('Lot %s contains an issue in verification' % outfile.lotnum)
        outlot.save()
