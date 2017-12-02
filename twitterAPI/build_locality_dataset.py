from functions import *

if __name__ == "__main__":
    locality_ds = readNeighborhoods()
    locality_ds = readStreets(locality_ds)
    
    with open('../dataset/locality_ds.json', 'w+') as f:
        f.write(json.dumps(locality_ds,indent=2))
