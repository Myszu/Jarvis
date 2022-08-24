import csv

def to_dict(file):
    data = []

    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        
        for row in csv_reader:
            data.append(row)
            
    return data


def to_list(file):
    users = []

    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        
        for row in csv_reader:
            users.append(row[0])
            
    return users


def to_file(content, file='output'):
    with open(file, 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        for row in content:
            writer.writerow(row)