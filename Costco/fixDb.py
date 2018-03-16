import config

import BStockImages.util.db.dbmongo as dbm


if __name__ == '__main__':
    client = dbm.getClient()
    db = client.Items

    dbfrom = db.costco
    # Change to capital letter
    dbto   = db.Costco

    # Get everything in db
    dbitems = dbfrom.find({})

    for ccitem in dbitems:
        # Check if item already exists in new db
        dup = dbto.find({'itemnumber' : ccitem['item-num']})
        if dup != None and dup['found'] and dup['searched'] and \
            if 'reasons' in dup and 'reasons' in ccitem:
                if 'website' in dup and 'website' not in ccitem:
                    continue
                elif 'website' in ccitem and 'website' not in dup:
                   # Fix  
                    

