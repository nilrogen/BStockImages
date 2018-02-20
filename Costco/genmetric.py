import config


import pymongo

def writevalue(csvout, item):
    if 'reasons' in item:
        reason = item['reasons']
        csvout.writerow([item['item-num'], reason['ratio'], item['description'], \
                        reason['description'], '=HYPERLINK(\"%s\")'%reason['imglink']])


if __name__ == '__main__':
    client = pymongo.MongoClient('192.168.1.13')
    db = client.Items
    col = db.costco

    items = col.find({ 'found': True, 'searched' : True})
    items.sort('reasons.ratio', 1)

    #print(len(list(items)))

    with open('output.csv', 'w') as fout:
        import csv
        csvout = csv.writer(fout)
        csvout.writerow(['Item number','Ratio','Description', 'Image Description','Image Link'])
        for item in items:
            writevalue(csvout,item)




