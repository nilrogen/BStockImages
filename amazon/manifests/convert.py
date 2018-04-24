import sys, os
from os.path import *
sys.path.append(os.getenv('HOME'))

from BStockImages.CostcoOld.config import _DROPBOX_PATH

import glob
import xlrd
import csv


_PATH = join(_DROPBOX_PATH, 'Marketplace Images/Amazon Manifest/Additional Manifests')

if __name__ == '__main__':
    files = glob.glob(join(_PATH, '*.xlsx'))
    for fname in files:
        name, ext = splitext(basename(fname))

        xlsx = xlrd.open_workbook(fname)
        sheet = xlsx.sheet_by_index(0)

        with open(name + '.csv', 'w', newline='', encoding='utf-7') as fout:
            writer = csv.writer(fout, quoting=csv.QUOTE_ALL)
            for i in range(sheet.nrows):
                writer.writerow(sheet.row_values(i))
