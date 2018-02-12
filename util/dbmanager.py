from BStockImages.util.dbobjects import *
from BStockImages.util.config import *

import MySQLdb as sql

fout = open('out.sql', 'w')

class DBManager(object):
    def __init__(self, connection, mktpName):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.mktpName = mktpName
        self.idMarketplace = self.getidMarketplace()
        self.itemfields = None
        self.itemdesfields = None
        if self.idMarketplace is None:
            raise ValueError('mktpName was not found in Table Marketplace')

    def addInformation(self, item, itemdes):
        """
        " Use this method to check and add both an Item and ItemDescription
        " objects to their respective tables. 
        " 
        " First it checks if the item already exists, adding to both the
        " Item and ItemDescription tables if not. 
        "
        " If the Item does exist then it updates the Item, then checks if there
        " is a related ItemDescription. It updates or adds to that table as 
        " necessary
        """
        if type(item) is not Item: 
            raise ValueError("Argument 'item' not of type Item.")
        if type(itemdes) is not ItemDescription:
            raise ValueError("Argument 'itemdes' not of type ItemDescription.")

        self.item = item
        self.itemdes = itemdes
        self.itemdes.setValue(idMarketplace, self.idMarketplace)
        self.itemdes.setValue(ModelNumber, item.getValue(ModelNumber))

        if not self.check_item_exists():
            self.add_item()
            self.add_itemdes()
        else:
            self.update_item()
            if not self.check_itemdes_exists():
                self.add_itemdes()
            else:
                self.update_itemdes()
    
    def getidMarketplace(self):
        query = '''SELECT idMarketplace 
                   FROM Marketplace
                   WHERE mktpName LIKE "%s"''' % self.mktpName

        self.cursor.execute(query)

        val = self.cursor.fetchone()
        if val is not None:
            val = val[0]
        return val

    """
    " These functions retrieve and set the Column Names for their respective
    " table.
    """
    def get_item_fields(self):
        if self.itemfields is not None:
            return self.itemfields
        query = "SHOW COLUMNS FROM Item";
        self.cursor.execute(query)

        self.itemfields = list(map(lambda x: x[0], self.cursor.fetchall()))
        return self.itemfields

    def get_itemdes_fields(self):
        if self.itemdesfields is not None:
            return self.itemdesfields
        query = "SHOW COLUMNS FROM ItemDescription";
        self.cursor.execute(query)

        self.itemdesfields = list(map(lambda x: x[0], self.cursor.fetchall()))
        return self.itemdesfields
            

    def check_item_exists(self):
        query = '''SELECT * 
                   FROM Item
                   WHERE ModelNumber LIKE %s
                ''' % self.item.getSQLValue(ModelNumber)
        self.cursor.execute(query)

        return self.cursor.fetchone() != None

    def check_itemdes_exists(self):
        query = '''SELECT * 
                   FROM ItemDescription
                   WHERE ModelNumber LIKE %s
                   AND idMarketplace = %s
                ''' % (self.item.getSQLValue(ModelNumber), 
                       self.idMarketplace)
        self.cursor.execute(query)

        return self.cursor.fetchone() != None

    def add_item(self):
        query = 'INSERT INTO Item (%s) VALUES (%s)'

        cn, cv = '', ''

        for k in self.item.__dict__:
            cn += k + ', '
            cv += self.item.getSQLValue(k) + ', '
        cn, cv = cn[:-2], cv[:-2]

        query = query % (cn, cv)
        self.cursor.execute(query)
        fout.write(query + ';\n')
        self.connection.commit()

    def add_itemdes(self):
        query = 'INSERT INTO ItemDescription (%s) VALUES (%s)'
        cn, cv = '', ''

        for k in self.itemdes.__dict__:
            cn += k + ', '
            cv += self.itemdes.getSQLValue(k) + ', '
        cn, cv = cn[:-2], cv[:-2]

        query = query % (cn, cv)

        self.cursor.execute(query)
        fout.write(query + ';\n')
        self.connection.commit()

    def get_item(self):
        """
        " This method SELECTS the requested item from the table
        " and returns a dbobjects.Item object
        """
        query = '''SELECT * 
                    FROM Item 
                    WHERE ModelNumber LIKE %s
                ''' % self.item.getSQLValue(ModelNumber)
        
        itemrows = self.get_item_fields()
        self.cursor.execute(query)

        itemdict = dict(zip(itemrows, self.cursor.fetchone()))
        ritem = Item.load_values(itemdict)
        return ritem

    def get_itemdes(self):
        query = '''SELECT * 
                    FROM ItemDescription
                    WHERE ModelNumber LIKE %s
                    AND idMarketplace = %s
                ''' % (self.itemdes.getSQLValue(ModelNumber), 
                       self.idMarketplace)
        
        itemdesrows = self.get_itemdes_fields()
        self.cursor.execute(query)

        itemdict = dict(zip(itemdesrows, self.cursor.fetchone()))
        ritem = ItemDescription.load_values(itemdict)
        return ritem
        
    def update_item(self):
        """
        " The idea for update is to first get the item in the table.
        " then add information to it that does not exist already.
        """
        query = 'UPDATE Item SET %s WHERE ModelNumber LIKE %s'

        # Get Item from Table and add any values not present
        # FIXME: Its possible that the way adding two items together
        # Needs to be fixed.
        itm = self.get_item()
        self.item = itm.addTo(self.item)
        
        # generate <column-name> = <column-value> string
        cc = ''
        for key in self.item.__dict__:
            if self.item.valueChanged(key):
                cc += '%s = %s, ' % (key, self.item.getSQLValue(key))

        # Check if any columns are to be updated
        if cc == '':
            return
        cc = cc[:-2] # get rid of ', ' at end

        query = query % (cc, self.item.getSQLValue(ModelNumber))
        fout.write(query + ';\n')
        self.cursor.execute(query)
        self.connection.commit()

    def update_itemdes(self):
        """
        " The idea for update is to first get the ItemDescription 
        " in the table. Then add information to it that does not 
        " exist already.
        """
        query = 'UPDATE ItemDescription SET %s ' + \
                'WHERE ModelNumber LIKE %s AND idMarketplace = %s'

        # Get ItemDescription from Table and add any values not present.
        # FIXME: Its possible that the way adding two items together
        # Needs to be fixed.
        itm = self.get_itemdes()
        self.itemdes = itm.addTo(self.itemdes)
        
        # generate <column-name> = <column-value> string
        cc = ''
        for key in self.itemdes.__dict__:
            if self.itemdes.valueChanged(key):
                cc += '%s = %s, ' % (key, self.itemdes.getSQLValue(key))

        # Check if any columns are to be updated
        if cc is '':
            return
        cc = cc[:-2] # get rid of ', ' at end
        
        query = query % (cc, self.item.getSQLValue(ModelNumber), self.idMarketplace)
        fout.write(query + ';\n')
        self.cursor.execute(query)
        self.connection.commit()

