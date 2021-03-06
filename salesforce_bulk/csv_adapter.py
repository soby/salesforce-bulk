import unicodecsv as csv
from io import BytesIO

class CsvDictsAdapter(object):
    """Provide a DataChange generator and it provides a file-like object which returns csv data"""
    def __init__(self, source_generator):
        self.source = source_generator
        self.buffer = BytesIO()
        self.csv = None
        self.add_header = False

    def __iter__(self):
        return self

    def write_header(self):
        self.add_header = True

    def next(self):
        row = self.source.next()

        self.buffer.truncate(0)
        self.buffer.seek(0)

        if not self.csv:
            self.csv = csv.DictWriter(self.buffer, row.keys(), quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8')
            self.add_header = True
        if self.add_header:
            if hasattr(self.csv, 'writeheader'):
                self.csv.writeheader()
            else:
                self.csv.writerow(dict((fn, fn) for fn in self.csv.fieldnames))
            self.add_header = False

        self.csv.writerow(row)
        self.buffer.seek(0)
        return self.buffer.read()
