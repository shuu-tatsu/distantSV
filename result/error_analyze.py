import sys


class ErrorAnalyzer():

    def __init__(self, known_ne, unk_ne, result_file_list):
        self.known_ne_set = known_ne
        self.unk_ne_set = unk_ne
        self.result_output_list = read_file(result_file_list)
        self.known_occurrences = 0
        self.unk_occurrences = 0

        self.FN_known_error = 0
        self.FN_unk_error = 0
        self.FP_known_error = 0
        self.FP_unk_error = 0

    def count_gold(self, word):
        if word in self.known_ne_set:
            self.known_occurrences += 1
        elif word in self.unk_ne_set:
            self.unk_occurrences += 1
        else:
            print('No both sets in count_gold')

    def count(self):
        for output in self.result_output_list:
            try:
                word, gold, pred = output.split()
                if gold != 'O':
                    self.count_gold(word)
                if gold != pred:
                    self.count_error(word, gold, pred)
            except ValueError:
                pass
        self.get_error_probability()

    def count_error(self, word, gold, pred):
        if gold == 'O':
            self.count_FN_error(word)
        else:
            self.count_FP_error(word)

    def count_FN_error(self, word):
        if word in self.known_ne_set:
            self.FN_known_error += 1
        elif word in self.unk_ne_set:
            self.FN_unk_error += 1
        else:
            print('No both sets in count_FN')

    def count_FP_error(self, word):
        if word in self.known_ne_set:
            self.FP_known_error += 1
        elif word in self.unk_ne_set:
            self.FP_unk_error += 1
        else:
            print('No both sets in count_FP')

    def get_error_probability(self):
        #FN error
        #Known error
        self.FN_known_error_prob = division(self.FN_known_error, self.known_occurrences)
        #Unk error
        self.FN_unk_error_prob = division(self.FN_unk_error, self.unk_occurrences)

        #FP error
        #Known error
        self.FP_known_error_prob = division(self.FP_known_error, self.known_occurrences)
        #Unk error
        self.FP_unk_error_prob = division(self.FP_unk_error, self.unk_occurrences)


class Vocabulary():

    def __init__(self, file_list):
        self.word_label_list = read_file(file_list)
        self.vocab_set, self.vocab_size = self.make_ne_list()

    def make_ne_list(self):
        vocab = set()
        for line in self.word_label_list:
            try:
                word, label = line.split()
                if label != 'O':
                    vocab.add(word)
            except ValueError:
                pass
        return vocab, len(vocab)


def read_file(file_list):
    word_label_list = []
    for file_path in file_list:
        with open(file_path, 'r') as r:
            word_label_list.extend([line for line in r])
    return word_label_list


def division(denominator, numerator):
    try:
        answer = denominator / numerator
    except ZeroDivisionError:
        answer = -1
    return answer


def main():
    data_folder = '/cl/work/shusuke-t/distantSV/corpus/medline/conllform/'
    TRAIN_FILE = data_folder + 'cross_validation/train_conllform_1and2.txt'
    DEV_FILE = data_folder + 'cross_validation/train_conllform_3.txt'
    TEST_FILE = data_folder + 'full_test_conllform.txt'
    #RESULT_FILE = '/cl/work/shusuke-t/flair_myLM_normal/resources/taggers/cross_validation_log_full_baseline/test.tsv'
    RESULT_FILE = '/cl/work/shusuke-t/flair_myLM_normal/resources/taggers/cross_validation_log_full_tp_0107/test.tsv'
    #RESULT_FILE = '/cl/work/shusuke-t/flair_myLM_normal/resources/taggers/cross_validation_log_baseline/test.tsv'

    known_ne = Vocabulary([TRAIN_FILE, DEV_FILE])
    print('Known NE set size: {}'.format(known_ne.vocab_size))
    unk_ne = Vocabulary([TEST_FILE])
    print('Unk NE set size: {}'.format(unk_ne.vocab_size))

    analyser = ErrorAnalyzer(known_ne.vocab_set, unk_ne.vocab_set, [RESULT_FILE])
    analyser.count()
    print('Known occurrences: {}'.format(analyser.known_occurrences))
    print('Unk occurrences: {}'.format(analyser.unk_occurrences))
    print('FN known error prob: {} FN unk error prob: {}'.format(analyser.FN_known_error_prob, analyser.FN_unk_error_prob))
    print('FP known error prob: {} FP unk error prob: {}'.format(analyser.FP_known_error_prob, analyser.FP_unk_error_prob))


if __name__ == '__main__':
    main()
