import sys
import json
# from CPLDirect import *
import CPL
# from CPL import NONE

db_connection = CPL.cpl_connection()


def import_prov(filename):
    with open(filename, 'r') as f:
        # return json.load(f)
        return f.read()

def pipe2cpl(json_string):
    # print(type(json_string))
    db_connection.import_document_json(json_string, "advocacy")
    # print(CPL_NONE)
    # import_document_json(json_string, "advocacy")

def main():
    # pipe2cpl(import_prov(sys.argv[1]))
    pipe2cpl(import_prov('../json_examples/prov_advocacy/prov.json'))

if __name__=='__main__':
    main()
