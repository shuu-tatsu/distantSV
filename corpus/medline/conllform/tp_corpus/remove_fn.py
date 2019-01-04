import sys


class OutputCorpus():

    def __init__(self, words_list):
        self.words_list = words_list

    def split_by_sentence(self):
        self.all_sentences_list = []
        one_sentence_list = []
        for word in self.words_list:
            if word[0] == '\n':
                # センテンス末のトークン
                self.all_sentences_list.append(one_sentence_list)
                one_sentence_list = []
            else:
                # センテンス中のトークン
                one_sentence_list.append(word)
        '''
        self.all_sentences_list:
        [[['This', 'O', 'O\n'], ['change', 'O', 'O\n'], ...,[')', 'O', 'O\n'], ['.', 'O', 'O\n']], [['Both', 'O', 'O\n'], ...,['assays', 'O', 'O\n'], ['.', 'O', 'O\n']]]
        '''

    def remove_fn_sentences(self):
        self.tp_sentences_list = []
        for sentence in self.all_sentences_list:
            if self.judge_sentence(sentence):
                self.tp_sentences_list.append(sentence)
        return self.tp_sentences_list

    def judge_sentence(self, sentence):
        # fnなトークンが全く無ければ，return True
        # fnなトークンが一つでもあれば，return False
        for word in sentence:
            if self.judge_word(word):
                pass
            else:
                return False
        return True

    def judge_word(self, word):
        token = word[0]
        gold_tag = word[1]
        predicted_tag = word[2].strip('\n')
        if gold_tag == predicted_tag:
            return True
        else:
            return False


def load(read_file):
    with open(read_file, 'r') as r:
        words_list = [word.split(' ') for word in r]
    return words_list
    '''
    words_list:
    [..., ['.', 'O', 'O\n'], ['\n'], ['We', 'O', 'O\n'], ['have', 'O', 'O\n'], ..., ['cells', 'O', 'O\n'], ['in', 'O', 'O\n']]
    '''

def write(write_file, tp_sentences_list):
    with open(write_file, 'w') as w:
        for sentence in tp_sentences_list:
            write_sentence(w, sentence)


def write_sentence(w, sentence):
    for word in sentence:
        token = word[0]
        gold_tag = word[1]
        seq = token + ' ' + gold_tag + '\n'
        w.write(seq)
    w.write('\n')


def main(read_file, write_file):
    words_list = load(read_file)
    output_corpus = OutputCorpus(words_list)
    output_corpus.split_by_sentence()
    tp_sentences_list = output_corpus.remove_fn_sentences()
    write(write_file, tp_sentences_list)


if __name__ == '__main__':
    args = sys.argv
    read_file = args[1]
    write_file = args[2]
    main(read_file, write_file)
