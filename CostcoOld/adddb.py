import procman as pm
import pymongo 


if __name__ == '__main__':
    client = pymongo.MongoClient('192.168.1.13')

    db = client.Items
    costco = db.costco

    values = pm.getItemJson()['items']
    print(type(values))

    #costco.insert_many(values)








