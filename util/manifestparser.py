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
    def __init__(self, fin, columndict, default=None):
        self.reader = csv.reader(fin)
        self.columndict = dict.fromkeys(columndict, None)
        self.defaults = dict.fromkeys(self.columndict, default)
        self._setColumnDefaults(columndict)


    def _setColumnDefaults(self, columndict):
        for key in columndict:
            value = columndict[key]
            if type(value) != list:
                value = [value]
            self.columndict[key] = []
            for elm in value:
                if type(elm) == tuple:
                    self.columndict[key].append(elm[0])
                    self.defaults[key] = elm[1]
                else:
                    self.columndict[key].append(elm)

    def getColumns(self):
        firstline = next(self.reader)
        retv = dict.fromkeys(self.columndict.keys(), -1)

        for key in self.columndict:
            for index in range(len(firstline)):

                value = self.columndict[key]
                if type(value) == str and value == firstline[index]:
                    retv[key] = index
                    break

                if type(value) == list:
                    for elem in value:
                        if type(elem) == str and elem == firstline[index]:
                            retv[key] = index
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
                    if value.strip() == '':
                        retv[key] = self.defaults[key]
                    else:
                        retv[key] = value
                else:
                    retv[key] = self.defaults[key]
            yield retv
        raise StopIteration()
