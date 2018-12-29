import csv

def load(read_file):
    with open(read_file, 'r') as r:
        reader = csv.reader(r)
        l = [ne for ne in reader]
    ne_list = [ne[0] for ne in l]
    return ne_list

def make_vocab(write_file, ne_list):
    with open(write_file, 'w') as w:
        for line in ne_list:
            w.write(line)
            w.write('\n')

all_ne_list = []
read_file = 'CTD_chemicals.csv'
all_ne_list.extend(load(read_file))

read_file = 'CTD_diseases.csv'
all_ne_list.extend(load(read_file))

write_file = 'ctd_vocab.txt'
make_vocab(write_file, all_ne_list)
