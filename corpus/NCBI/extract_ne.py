import re

absts_list = []
read_file_list = ['NCBI_corpus_development.txt', 'NCBI_corpus_testing.txt', 'NCBI_corpus_training.txt']
for read_file in read_file_list:
    with open(read_file, 'r') as r:
        read_list = [abst for abst in r]
        absts_list.extend(read_list)

ne_list = [] # [(Type, ne), (), (), ...]
for abst in absts_list:
    ne_list.extend(re.findall('<category="([^<]+?)">([^"]+?)</category>', abst))
vocab = [ne_tuple[1] for ne_tuple in ne_list]

with open('ncbi_vocab.txt', 'w') as w:
    for word in vocab:
        w.write(word)
        w.write('\n')
