#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tqdm import tqdm
from flashtext import KeywordProcessor
import random


class Annotation():

    def __init__(self, TRAIN_FILE, DEV_FILE, eval_file_list, DICT_FILE):
        self.train_file = TRAIN_FILE
        self.dev_file = DEV_FILE
        self.eval_file1 = eval_file_list[0]
        self.eval_file2 = eval_file_list[1]
        self.dict_file = DICT_FILE

    def devide_vocab(self, rate=0.8):
        #Dictionary をソートし、rateに従ってtrain(devも供用)とevalに分ける。
        with open(self.dict_file, 'r') as r:
            words_duplication_list = [word.strip('\n') for word in r]
        words_list = remove_duplication(words_duplication_list)
        random.shuffle(words_list)
        train_vocab_size = int(len(words_list) * rate)
        self.train_vocab_list = words_list[:train_vocab_size]
        self.dev_vocab_list = self.train_vocab_list

        self.eval1_vocab_list = words_list[train_vocab_size:]
        self.eval2_vocab_list = words_list

    def make_annotation(self):
        make_anno_corpus(self.train_vocab_list, self.train_file)
        make_anno_corpus(self.dev_vocab_list, self.dev_file)

        make_anno_corpus(self.eval1_vocab_list, self.eval_file1)
        make_anno_corpus(self.eval2_vocab_list, self.eval_file2)


def make_anno_corpus(vocab_list, target_corpus):
    #NE抽出器生成
    keyword_processor = make_ne_founder(vocab_list)
    #データからNEを抽出
    extracted_words_list = extract_keywords(target_corpus, keyword_processor) 
    #Write annotation file
    write_file = target_corpus[:-4] + '_anno_' + target_corpus[-4:]
    write_annotation(extracted_words_list, write_file)


def write_annotation(extracted_words_list, write_file):
    with open(write_file, 'w') as w:
        for sent_id, keywords_found_list in extracted_words_list:
            for keywords_found in keywords_found_list:
                w.write(sent_id + '\t')
                w.write(str(keywords_found[0]) + '\t')
                w.write(str(keywords_found[1]) + '\t')
                w.write(str(keywords_found[2]))
                w.write('\n')


def make_ne_founder(vocab_list):
    keyword_processor = KeywordProcessor(case_sensitive=True)
    for vocab in tqdm(vocab_list):
        keyword_processor.add_keyword(vocab)
    return keyword_processor

'''
sent_id
29600
sentence
Plasma profiles of luteinizing hormone (LH), testosterone (T), and estradiol (E2) have been determined in five mature rams during the primary breeding season (September) and again when breeding activity was low (May).

keywords_found
[('Luteinizing Hormone', 19, 38), ('Testosterone', 45, 57), ('Estradiol', 67, 76)]
'''


def extract_keywords(target_corpus, keyword_processor):
    with open(target_corpus, 'r') as r:
        sentences = [sentence.split('\t') for sentence in r]
    extracted_words_list = []
    for sent_id, sentence in tqdm(sentences):
        keywords_found_list = keyword_processor.extract_keywords(sentence, span_info=True)
        extracted_words_list.append((sent_id, keywords_found_list))
    return extracted_words_list


def remove_duplication(words_list):
    words_set = set(words_list)
    words_noduplication_list = [word for word in words_set]
    return words_noduplication_list


def labeling_id(target_file, train_file, dev_file, eval_file):
    file_list = [train_file, dev_file, eval_file]
    for data_file in file_list:
        write_file = target_file + 'id_' + data_file[len(target_file):]
        with open(data_file, 'r') as r, open(write_file, 'w') as w:
            sentence_id = 1
            for sentence in r:
                line = str(sentence_id) + '\t' + sentence
                w.write(line)
                sentence_id += 1

'''
[['1', 'Primer extension and subsequent PCR amplification of these in vitro transcripts revealed gamma-thio-ATP-dependent, but no beta-thio-ATP-dependent, signals, although affinity labelling of overall in vitro transcripts still occurred with beta-thio-ATP.\n'], ['2', 'We conclude that the described plant nuclei reinitiated transcription non-specifically and that post-transcriptional transfer of the gamma-thio affinity label severely interfered with the detection of reinitiated transcripts..\n'], ['3', 'The location of gene expression of the Agrobacterium tumefaciens ipt gene promoter in transgenic tobacco plants was examined using the beta-glucuronidase (GUS) reporter gene.\n']]
[['6', 'Chloramphenicol', '213', '228'], ['10', 'NADP', '32', '36'], ['16', 'Amino Acids', '32', '43']]
'''


def main(TARGET_FILE, DICT_FILE):
    make_id_corpus = False
    if make_id_corpus:
        TRAIN_FILE = TARGET_FILE + 'train.txt' 
        DEV_FILE = TARGET_FILE + 'valid.txt'
        EVAL_FILE = TARGET_FILE + 'test.txt'
        labeling_id(TARGET_FILE, TRAIN_FILE, DEV_FILE, EVAL_FILE)

    make_anno_corpus = True
    if make_anno_corpus:
        TRAIN_FILE = TARGET_FILE + 'dir_id_train/id_train_split.txt' 
        DEV_FILE = TARGET_FILE + 'id_valid.txt'
        EVAL_FILE1 = TARGET_FILE + 'dir_id_test/id_test1.txt'
        EVAL_FILE2 = TARGET_FILE + 'dir_id_test/id_test2.txt'
        eval_file_list = [EVAL_FILE1, EVAL_FILE2]

        anno = Annotation(TRAIN_FILE, DEV_FILE, eval_file_list, DICT_FILE)
        anno.devide_vocab()
        anno.make_annotation()


if __name__ == '__main__':
    TARGET_FILE = '/cl/work/shusuke-t/distantSV/corpus/medline/'
    DICT_FILE = '/cl/work/shusuke-t/distantSV/pseudo_corpus/data/ctd_meshsupp_vocab.txt'
    main(TARGET_FILE, DICT_FILE)
