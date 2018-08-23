import csv
import os
from os.path import *

from argparse import *

HEADERS = ['Sub', 'Lot', 'Line', 'Sku', 'Product Description', 
           'Qty', 'Std Cost', 'Weight']

class Manifest:
    def __init__(self, palletnum, city):
        self.outfile = '%s %s.csv' % (palletnum, city)
        self.palletnum = palletnum
        self.values = [HEADERS]

    def fixnum(self, value):
        retv = ''
        for c in str(value):
            if c.isdigit() or c == '-' or c == '.':
                retv += c
        return float(retv)

    def addValue(self, value):
        if len(value) != 8:
            if len(value[1]) != 4:
                fv = [value[1][:4], value[1][3:]]
                value = value[:1] + fv + value[2:]
            
        value[5] = int(self.fixnum(value[5])) # QTY
        value[6] = self.fixnum(value[6])      # Cost
        value[7] = self.fixnum(value[7])      # Weight

        for i in range(1, len(self.values)):
            if value[:5] == self.values[i][:5]:
                self.values[i][5] += value[5] # QTY
                self.values[i][6] += value[6] # Cost
                self.values[i][7] += value[7] # Weight
                return
        self.values.append(value)

    def save(self):
        sfn = lambda val: val[6]
        self.values[1:] = sorted(self.values[1:], key=sfn, reverse=True)
        with open(self.outfile, 'w') as fout:
            writer = csv.writer(fout, dialect=csv.unix_dialect)
            writer.writerows(self.values)
        print('Saved ', self.outfile)
        
def splitLine(line):
    retv = []

    splt = line.split(chr(0xa0))
    if len(splt) != 1:
        for val in splt:
            if val != '':
                retv.append(val.strip())
    else:
        splt = line.split('  ')
        for val in splt:
            if val != '':
                retv.append(val.strip())
    return retv 

def typeLine(splitline):
    return len(splitline) == 5 and splitline[-1] != 'Weight'

def fixLine(splitline):
    val = splitline[0].split(' ')
    if len(val) == 2:
        val.extend(['', ''])
    val.extend(splitline[1:])

    for i in range(len(val)):
        if val[i] == '':
            val[i] = 'N/A'
        val[i] = val[i].strip()
    return val

def processManifest(manifestname, outdir):
    curdir = os.getcwd()

    with open(manifestname, 'r') as fin:
        os.chdir(outdir)

        palletnum, city = splitext(basename(fin.name))[0].split(' ')
        curmanifest = Manifest(palletnum, city)

        print('Processing ', manifestname, flush=True)

        for line in fin:
            # Split Line based on char 160 or 2 spaces
            spline = splitLine(line)

            # Check line type
            if typeLine(spline):
                spline = fixLine(spline)
                curmanifest.addValue(spline)
    
        curmanifest.save()

    os.chdir(curdir)

if __name__ == '__main__':
    parser = ArgumentParser('JC Penney Script')
    parser.add_argument('-o', dest='outdir', help='Output Directory')
    parser.add_argument('manifests', nargs='+', help='Bad Manifests')

    args = parser.parse_args()

    outdir = None
    if args.outdir:
        if not os.path.isdir(args.outdir):
            os.mkdir('outdir')
        outdir = args.outdir
    else:
        if not os.path.exists('output'):
            os.mkdir('output')
        outdir = 'output'
    
    for manifest in args.manifests:
        if os.path.exists(manifest):
            processManifest(manifest, outdir)
        else:
            print(manifest, 'does not exist.')
