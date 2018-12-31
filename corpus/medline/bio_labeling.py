#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tqdm import tqdm
import sys

def preprocessing(sentence):
    sentence = sentence.replace(', ', ' , ')
    sentence = sentence.replace('. ', ' . ')
    sentence = sentence.replace('; ', ' ; ')
    sentence = sentence.replace('.\n', ' . ')
    sentence = sentence.split(' ')
    return sentence


def judge(ne_abs_id_list, abs_id):
    if abs_id in ne_abs_id_list:
        return True
    else:
        return False


def o_token_processing(s_index, e_index, abs_sent):
    #NE以外のセンテンス処理
    if e_index == 'end':
        sentence = abs_sent[s_index:]
    else:
        sentence = abs_sent[s_index:e_index]
    token_list = preprocessing(sentence)

    if len(token_list[0]) == 0:
        return token_list[1:]
    else:
       return token_list


def update_start_index(ne_end_index, char_or_space):
    #NE後がスペースか文字かで分岐
    if char_or_space != ' ':
        #print('################')
        #print(char_or_space)
        #print(len(char_or_space))
        #print(type(char_or_space))
        #print('################')
        #文字なら次ステップへ伝達
        return ne_end_index
    else:
        #スペースなら切り捨てる
        return ne_end_index+1


def bio_labeling(abs_sent, start_index, ne, labeled_token_list, ne_no, last_ne_no):
    ne_start_index = int(ne[2])
    ne_end_index = int(ne[3])
    #print('ne_start_index:{}  ne_end_index{}'.format(ne_start_index, ne_end_index))
    #NE以外のセンテンス処理
    #print('#NE以外のセンテンス処理')
    o_token_list = o_token_processing(start_index, ne_start_index-1, abs_sent)
    #print('o_token_list:{}'.format(o_token_list))
    labeled_token_list.extend(o_labeling(o_token_list))
    #print('labeled_token_list:{}'.format(labeled_token_list))
    #NEの処理
    #print('#NEの処理')
    ne_token_list = preprocessing(abs_sent[ne_start_index:ne_end_index])
    #print('ne_token_list:{}'.format(ne_token_list))
    labeled_token_list.extend(bi_labeling(ne_token_list))
    #print('labeled_token_list:{}'.format(labeled_token_list))

    next_start_index = update_start_index(ne_end_index, abs_sent[ne_end_index])

    if ne_no == last_ne_no:
        #NE以外のセンテンス処理
        #print('#NE以外のセンテンス処理 in last')
        o_token_list = o_token_processing(next_start_index, 'end', abs_sent)
        #print('o_token_list:{}'.format(o_token_list))
        labeled_token_list.extend(o_labeling(o_token_list))
        #print('labeled_token_list:{}'.format(labeled_token_list))
        #print('\n\n')
        return labeled_token_list, 'end'

    return labeled_token_list, next_start_index


def o_labeling(token_list):
    labeled_token_list = []
    for token in token_list:
        if len(token) > 0:
            string = token + '\tO'
        else:
            string = token
        labeled_token_list.append(string)
    return labeled_token_list


def bi_labeling(token_list):
    labeled_ne_list = []
    for i, token in enumerate(token_list):
        if i == 0:
            string = token + '\tB'
        else:
            string = token + '\tI'
        labeled_ne_list.append(string)
    #print('labeled_ne_list in def bi_labeling() : {}'.format(labeled_ne_list))
    return labeled_ne_list


'''
l = "To further examine the transcriptional basis of this broad expression pattern, deletions in the 5' non-coding region of the gene were translationally fused to two promoterless reporter genes, encoding the enzymes chloramphenicol acetyl transferase (CAT) and beta-glucuronidase (GUS).\n"

l[213:228]
'chloramphenicol'
'''

def write_file(w, token_list):
    for token in token_list:
        w.write(token)
        w.write('\n')


'''
コマンドライン引数には0~101の数字を入れる
'''
ne_sent_only = True

args = sys.argv
id_train_file = '/cl/work/shusuke-t/distantSV/corpus/medline/dir_id_train/split_id_' + str(args[1]) + '.txt'
id_train_anno_file = '/cl/work/shusuke-t/distantSV/corpus/medline/dir_id_train_anno/split_anno_' + str(args[1]) + '.txt'
train_conllform_file = '/cl/work/shusuke-t/distantSV/corpus/medline/conllform/dir_train_conllform/train_conllform_' + str(args[1]) + '.txt'

#with open('id_test.txt', 'r') as r1, open('id_test_anno_.txt', 'r') as r2:
#with open('id_valid.txt', 'r') as r1, open('id_valid_anno_.txt', 'r') as r2:
#with open('id_train.txt', 'r') as r1, open('id_train_anno_.txt', 'r') as r2:
with open(id_train_file, 'r') as r1, open(id_train_anno_file, 'r') as r2:
    absts = [line.split('\t') for line in r1]
    annos = [line.strip('\n').split('\t') for line in r2]
    ne_abs_id_list = [int(i[0]) for i in annos]

#w = open('test_conllform.txt', 'w')
#w = open('valid_conllform.txt', 'w')
#w = open('train_conllform.txt', 'w')
w = open(train_conllform_file, 'w')
for abs_id, abs_sent in tqdm(absts):
    #print('abs_sent:{}'.format(abs_sent))
    if judge(ne_abs_id_list, int(abs_id)):
        #This abst includes NE.
        ne_index_list = [i for i, ne_abs_id in enumerate(ne_abs_id_list) if ne_abs_id == int(abs_id)]
        '''
        abs_sent:
        They are N-acetylglucosamine pentasaccharides of which the non-reducing residue is N-methylated and N-acylated with cis-vaccenic acid (C18:1) or stearic acid (C18:0) and carries...  

        ne_index_list:
        [52, 53, 54]
        '''
        next_start_index = 0
        labeled_token_list = [] #ラベル付けされたセンテンスを格納するリスト
        last_ne_no = len(ne_index_list)
        for i, ne_index in enumerate(ne_index_list):
            ne_no = i + 1
            labeled_token_list, next_start_index = bio_labeling(abs_sent, next_start_index, annos[ne_index], labeled_token_list, ne_no, last_ne_no)
        write_file(w, labeled_token_list)
    else:
        #This abst does not include NE.
        if ne_sent_only:
            pass
        else:
            labeled_token_list = o_labeling(preprocessing(abs_sent))
            write_file(w, labeled_token_list)

w.close()

'''
absts:
[['1', 'Primer extension and subsequent PCR amplification of these in vitro transcripts revealed gamma-thio-ATP-dependent, but no beta-thio-ATP-dependent, signals, although affinity labelling of overall in vitro transcripts still occurred with beta-thio-ATP.\n'], ['2', 'We conclude that the described plant nuclei reinitiated transcription non-specifically and that post-transcriptional transfer of the gamma-thio affinity label severely interfered with the detection of reinitiated transcripts..\n'], ['3', 'The location of gene expression of the Agrobacterium tumefaciens ipt gene promoter in transgenic tobacco plants was examined using the beta-glucuronidase (GUS) reporter gene.\n']]

annos:
[['6', 'Chloramphenicol', '213', '228'], ['10', 'NADP', '32', '36'], ['16', 'Amino Acids', '32', '43'], ['16', 'Ice', '108', '111'], ['16', 'Peptides', '173', '181']]
'''
