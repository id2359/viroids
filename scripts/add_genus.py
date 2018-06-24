import sys
import pandas as pd
from Bio import Entrez

def get_strain(feature_table):
    print feature_table
    for feature_dict in feature_table:
        if feature_dict["GBQualifier_name"] == 'strain':
            return feature_dict["GBQualifier_value"]

def get_record(accession):
    handle = Entrez.efetch(db="nucleotide", id=accession, retmode="xml")
    record = Entrez.read(handle)
    handle.close()
    return record

def get_family(record):
    d = record[0]
    return d['GBSeq_taxonomy'].split(";")[1]

def get_type(row):
    # this gets family which is pretty coarse
    accession = row['ACCID']
    record = get_record(accession)
    return get_family(record)

if __name__=='__main__':
    feature_file = sys.argv[1]
    new_name = feature_file.replace(".feature", ".with_family.feature")
    df = pd.read_csv(feature_file)
    df['TYPE'] = get_type(df['ACCID'])
    df.to_csv(new_name)
    






