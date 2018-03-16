import config

import pymongo

def writevalue(csvout, item):
    if 'reasons' in item:
        reason = item['reasons']

        lnk = '=HYPERLINK(\"{}\")'.format(reason['imglink'])
        print(lnk)
        row = [ item['item-num'], \
                reason['ratio'], \
                item['description'], \
                reason['description'], \
                lnk ]

        csvout.writerow(row)


if __name__ == '__main__':
    client = pymongo.MongoClient('192.168.1.13')
    db = client.Items
    col = db.costco

    items = col.find({ 'found': False, 'searched' : True, \
                       'reasons.description' : { '$exists' : True } })
    items.sort('reasons.ratio', 1)

    with open('badsearch.csv', 'w') as fout:
        import csv
        csvout = csv.writer(fout)
        csvout.writerow(['Item number','Ratio','Description', 'Image Description','Image Link'])
        for item in items:
            writevalue(csvout,item)




