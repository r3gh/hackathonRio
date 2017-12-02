import numpy as np
import pickle
import nltk
import csv
import re
import json
import io
import codecs
from unicodedata import normalize

def clean_str(s):
    s = normalize('NFKD', s).encode('ASCII','ignore').decode('ASCII')
    return re.sub('\W+','', s.lower() )

locality_ds = {}

def readNeighborhoods(locality_path = "../dataset/localidades.csv" ):
    file = io.open(locality_path, "r")
    localitys = file.readlines()
    for locality in localitys:
        key = clean_str(locality)
        if key not in locality_ds:
            locality_ds[key] = dict()
            locality_ds[key]["type"] = "neighborhood"
            locality_ds[key]["latlong"] = None
            locality_ds[key]["neighborhood_name"] = locality.strip()


def readStreets(locality_path="../dataset/LinkedGeoData.csv"):
    file = io.open(locality_path, "r")
    lines = file.readlines()
    for line in lines:
        row = line.split('\t')

        if len(row) <= 1:
            continue

        for i in range(0, len(row)):
            row[i] = row[i].replace("\n","")
            row[i] = row[i].replace("\"","")
            row[i] = row[i].strip()

        key = clean_str(row[2])
        if key not in locality_ds:
            locality_ds[key] = dict()
            locality_ds[key]["type"] = "street"
            locality_ds[key]["street_name"] = row[2].strip()
            if row[1] == '':
                locality_ds[key]["neighborhood_name"] = None
            else:
                locality_ds[key]["neighborhood_name"] = row[1].strip()

            if len(row) > 3:
                locality_ds[key]["latlong"] = [float(row[3]), float(row[4])]
            else:
                locality_ds[key]["latlong"] = None



if __name__ == "__main__":
    readNeighborhoods()
    readStreets()
    with open('../dataset/locality_ds.json', 'w+') as f:
        f.write(json.dumps(locality_ds,indent=2))
