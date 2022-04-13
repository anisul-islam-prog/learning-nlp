from excel_manager import ExcelManager
from mysql_manager import MySQLManager
from scibert import SciBERT
import numpy as np


EXCEL_FILENAMES = ["2021.xlsx"] # use 4 files to create 4 tables in database

def main():
    mysql = MySQLManager()
    scibert = SciBERT()
    for filename in EXCEL_FILENAMES:
        excel = ExcelManager(filename)
        data = excel.get()
        print("Inserting records from {}".format(filename))
        for i in range(len(data)):
            if i > 0 and i % 100 == 0:
                print("Inserted {} records into MySQL. ".format(i))
            record = {}
            record["author"] = data[i]["Authors"]
            try:
                vector = scibert.vectorize(data[i]["Abstract"])
            except:
                continue
            record["vector"] = vector.dumps()
            mysql.insert(record)
    mysql.close()


if __name__ == "__main__":
    main()
