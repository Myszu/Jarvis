import glob
import os
from .convert import to_file, to_dict

dataFile = 'input'
data = to_dict(f'data/{dataFile}.csv')

def splitFile(div):
    all = len(data)
    recs = int(all/div)
    for i in range(div):
        chunk = []
        if i != (div - 1):
            start = 1 + (i * recs) + i
            end = 1 + (i * recs) + i + recs
            print(f'Range {i+1} will be from {start} to {end}')
            chunk = data[start:end]
            to_file(chunk, f'output{i+1}')
        else:
            start = 1 + (i * recs) + i
            print(f'Range {i+1} will be from {start} to {all}')
            chunk = data[start:all]
            to_file(chunk, f'output{i+1}')
            

def getAllFiles():
    my_files = list()
    for root, dirs, files in os.walk("data\output"):
        for file in files:
            if file.endswith(".csv"):
                file_path= os.path.join(root, file) 
                my_files.append(file_path)
    return my_files


def deleteFiles(path, keyword):
    list_of_files = glob.glob(f'{path}/*') 
    for file in list_of_files:
        if file.find(keyword) >= 0:
            os.remove(file) 