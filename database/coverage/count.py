import unicodedata

'''
def load_chemdner(vocab_file):
    with open(vocab_file, 'r') as r:
        sentences = r.readlines()
        sentences2 = [l.strip() for l in sentences]
    word_list = []
    for sentence in sentences2:
        word_list.extend(sentence.split())
    vocab_set = set(word_list)
    print('{}:{}'.format(vocab_file, len(vocab_set)))
    return vocab_set
'''

def load_vocab_text(vocab_file):
    with open(vocab_file, 'r') as r:
        lines = r.readlines()
    words = [unicodedata.normalize("NFKC", word.split()[0]) for word in lines]
    vocab_set = set(words)
    print('{}:{}'.format(vocab_file, len(vocab_set)))
    return vocab_set


def culcurate_collocation(source_set, target_set):
    col = target_set & source_set
    trg = target_set - col
    src = source_set - col
    print('target:{}, collocation:{}, source:{}'.format(len(trg), len(col), len(src)))
    return col, trg, src


def main(source_file, target_file):
    source_set = load_vocab_text(source_file)
    target_set = load_vocab_text(target_file)
    col, trg, src = culcurate_collocation(source_set, target_set)
    #print('col')
    #print(col)
    #print('trg')
    #print(trg)
    #print('src')
    #print(src)

if __name__ == '__main__':
    source_file = 'ctd_meshsupp_vocab.txt'
    #source_file = 'pub_vocab.txt'
    #target_file = 'ncbi_vocab.txt'
    target_file = 'chemdner_eval_vocab.txt'
    main(source_file, target_file)
