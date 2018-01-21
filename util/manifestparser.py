import csv

class ManifestParserError(Exception):
    def __init__(self, msg):
        super(self, Exception)(msg)

class ManifestParser(object):
    """
    " After passing in a .csv file and columndict
    " This parses the csv file as an iterator.
    "
    " The Idea is to just mark which columns are important and return them.
    "
    " The format of the dictionary passed in is:
    "   <key> : <csv column name>
    " The output format is:
    "   <key> : <csv column value>
    " Where <key> is user defined (although usually a field name for
    " a table in the database. 
    "
    " This class works but could use some work possible.
    """ 
    def __init__(self, fin, columndict):
        self.reader = csv.reader(fin)
        self.columndict = columndict

    def getColumns(self):
        firstline = next(self.reader)
        retv = dict.fromkeys(self.columndict.keys(), -1)

        for key in self.columndict.keys():
            for index in range(len(firstline)):

                value = self.columndict[key]
                if type(value) == str and value == firstline[index]:
                    retv[key] = index
                    break

                if type(value) == list:
                    for elem in value:
                        if firstline[index] == elem.lower():
                            retv[key] = index
                            break
                if retv[key] != -1:
                    break
        return retv
                    
    def close(self):
        self.reader.close()

    def _error(self, msg):
        self.close()
        raise ManifestParserError(msg)

    def __iter__(self):
        return next(self)
    
    def __next__(self):
        columns = self.getColumns()
        
        for row in self.reader:
            retv = dict.fromkeys(columns.keys(), None)
            for key in columns:
                if columns[key] != -1:
                    value = row[columns[key]]
                    retv[key] = value
            yield retv
        raise StopIteration()
