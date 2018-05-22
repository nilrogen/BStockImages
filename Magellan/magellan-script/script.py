"""
" Magellan Input to Output Manifest Script.
"
" Author: Michael Gorlin
"""
import sys
import os
import glob
from argparse import *
import xlrd
import re
import csv


from pprint import *

LOT = re.compile('Lot ?ID')
QTY = re.compile('(Quantity|Units)')
ERT = re.compile('Ext\. Retail')

HEADER_NAMES = ['Category', 
                'Condition',
                'Product Number',
                'Item Description', 
                'Screen Size', 
                'Qty',
                'Retail', 
                'Ext. Retail',
                'Battery Type',
                'Battery Life',
                'Preloaded Maps',
                'Product Link']


OutputManifests = []
class OutputManifest:
    """
    " This class represents an output manifest. The script maintains a list of
    " these and saves the contents to their respective csv file after processing
    " all input manifests. 
    " 
    " When this object is created it loads the respective manifest if it exists
    " already. Data added to the manifest is checked against already existing
    " data, no exact duplicates are added.
    "
    " When the file is saved the rows are sorted by the "Ext. Retail" column
    """
    def __init__(self, lotnum, outdir):
        self.lotnum = lotnum
        self.outfile = os.path.join(outdir, 'Lot %d.csv' % lotnum)
        self.values = []
        self.load()

    def load(self):
        if os.path.exists(self.outfile):
            with open(self.outfile, 'r') as fin:
                reader = csv.reader(fin)
                for row in reader:
                    self.values.append(row)
        else:
            self.values = [HEADER_NAMES]

    def add(self, value):
        if value not in self.values:
            self.values.append(value)
    
    def save(self):
        # Find index of Ext. Retail
        erindex = self.values[0].index('Ext. Retail')
        # Sort by Ext. Retail
        keyfn = lambda row: float(row[erindex].strip('$'))
        self.values[1:] = sorted(self.values[1:], key=keyfn, reverse=True)

        # Write to file
        with open(self.outfile, 'w') as fout:
            writer = csv.writer(fout, dialect=csv.unix_dialect)
            writer.writerows(self.values)

    @staticmethod
    def get(lotnum):
        global OutputManifests
        outputman = None
        for om in OutputManifests:
            if om.lotnum == lotnum:
                outputman = om
        if outputman is None:
            outputman = OutputManifest(lotnum, outdir)
            OutputManifests.append(outputman)
        return outputman


def process_directories(dirlist, outdir):
    for d in dirlist:
        process_files(glob.glob(os.path.join(d, '*.xlsx')), outdir)

def process_files(manifests, outdir):
    for f in manifests:
        print('Processing -', f, end='')

        # Test if file exists and is an xlsx
        if not os.path.exists(f):
            print('- File does not exist', flush=True)
            continue
        elif os.path.splitext(f)[-1] != '.xlsx':
            print('- File is not a xlsx', flush=True)
            continue

        handle_manifest(f, outdir)

        print(flush=True) # Prints a newline and flushes stream.

def handle_manifest(manifest, outdir):
    global OutputManifests
    wb = xlrd.open_workbook(manifest)

    for sh in wb.sheets():
        headers = handle_headers(sh)
        # Check if 
        if headers == {}:
            continue
        # Loop through rows 
        for i in range(1, sh.nrows):
            row = sh.row_values(i)

            # Find OutputManifest object that matches lot number
            try:
                lotnum = int(row[headers['Lot #']])
            except:
                lotnum = int(row[headers['Lot #']].split()[-1])
            outputman = OutputManifest.get(lotnum)
             
            # Add values to the appropriate Output Manifest
            values = []
            for hname in HEADER_NAMES:
                if hname == 'Retail' or hname == 'Ext. Retail':
                    values.append('$%.2f' % row[headers[hname]])
                elif hname == 'Qty':
                    values.append('%d' % int(row[headers[hname]]))
                else:
                    values.append(row[headers[hname]])
            outputman.add(values) 
        
def handle_headers(sheet):
    """
    " This function maps the correct header values to the headers found in the sheet
    " Most of the values overlap through all sheets, however some do not.
    """
    row = sheet.row_values(0)
    retv = {}
    for i in range(len(row)):
        value = row[i]
        if LOT.search(value): # Matches lot #
            retv['Lot #'] = i
        elif QTY.search(value):
            retv['Qty'] = i
        elif ERT.search(value):
            retv['Ext. Retail'] = i
        elif value == 'Retail':
            retv['Retail'] = i
        elif value == 'Category':
            retv['Category'] = i
        elif value == 'Condition':
            retv['Condition'] = i
        elif value == 'Product Number':
            retv['Product Number'] = i
        elif value == 'Screen Size':
            retv['Screen Size'] = i
        elif value == 'Item Description':
            retv['Item Description'] = i
        elif value == 'Battery Type':
            retv['Battery Type'] = i
        elif value == 'Battery Life':
            retv['Battery Life'] = i
        elif value == 'Preloaded Maps':
            retv['Preloaded Maps'] = i
        elif value == 'Product Link':
            retv['Product Link'] = i

    return retv


if __name__ == '__main__':
    """
    " There are few command line arguments for this program. 
    "
    " The simplest is to pass in a list of input manifests:
    "   $ python script.py *.xlsx
    " 
    " Alternatively pass in a list of directories containing manifests:
    "   $ python script.py -d ManifestDir1/ ManifestDir2/
    "
    " The resulting output manifests will be created in the directory the
    " was run unless the -o argument is specified:
    "   $ python script.py -d ManifestDir/ -o OutputDir/
    "
    """
    parser = ArgumentParser('Input Manifest to Output Manifest converter.')
    parser.add_argument('-o', dest='outdir', help='Output Directory')
    parser.add_argument('-d', dest='indir', nargs='+')
    parser.add_argument('manifest', nargs='*')

    args = parser.parse_args()

    outdir = '.'
    if args.outdir:
        outdir = args.outdir
        if not os.path.isdir(outdir):
            os.mkdir(outdir)

    if args.indir:
        process_directories(args.indir, outdir)
    elif args.manifest != []:
        process_files(args.manifest, outdir)
   
    for outman in OutputManifests:
        outman.save()
