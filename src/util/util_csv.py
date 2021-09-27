import csv
import logging

def validate_column_headers_csv(csv_row, header, exception_type):
    for (label, column) in header.items():
        cell_value = csv_row[column].strip()
        if (label != 'Pixels' and label != cell_value) or (label == 'Pixels' and cell_value != ''):
            raise CsvException("{exception} exception. column: {col}, expected: '{expected}', actual: '{actual}'".format(
                exception=exception_type, col=column, expected=label, actual=cell_value
            ))



def load_csv(csv_file_path, with_header_row=True):
    logging.info("loading csv file '{}' ...".format(csv_file_path))

    data = {}

    with open(csv_file_path, newline='') as fil:
        line = 1
        header = None

        for row in csv.reader(fil):
            if line == 1:
                if with_header_row:
                    header = header_from_csv_row(row)
                else:
                    logging.error('support for "with_header_row=False" not implemented yet')

            else:
                row_data = extract_row_data_csv(header, row)
                row_key = "row:{}".format(line)
                data[row_key] = row_data

            line += 1
         
    return data


def header_from_csv_row(row):
    header = {}

    for i in range(len(row)):
        header[row[i]] = i
    
    return header


def extract_row_data_csv(header, row):
    row_data = {}

    for (attribute, column) in header.items():
        row_data[attribute] = row[column]

    return row_data

class CsvException(Exception):

    def __init__(self, message):
        self.err = message
        super().__init__(self.err)
