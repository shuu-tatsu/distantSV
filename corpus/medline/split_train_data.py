#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tqdm import tqdm


def make_init_list(no_abs_list, denominator):
    #分割する最初のabs_noのリストを作成(ファイルとファイルの境界作成)
    init_list = []
    for cnt, abs_no in enumerate(no_abs_list):
        if cnt % denominator == 0:
            init_list.append(abs_no)
    return init_list


def split(init_list, file_path):
    w = open(file_path[0], 'w')
    with open(file_path[1], 'r') as r:
        lines = [line for line in r]
    cnt = 0
    for line in lines:
        no = int(line.split('\t')[0])
        if no in init_list:
            init_list.remove(no)
            w.close()
            cnt += 1
            w = open(file_path[2] + str(cnt) + '.txt', 'w')
        w.write(line)
    w.close()


def split_anno(init_list):
    file_path = []
    file_path.append('./dir_id_train_anno/split_anno_0.txt')
    file_path.append('./dir_id_train_anno/id_train_split_anno_.txt')
    file_path.append('./dir_id_train_anno/split_anno_')
    split(init_list, file_path)


def split_id_train(init_list):
    file_path = []
    file_path.append('./dir_id_train/split_id_0.txt')
    file_path.append('./dir_id_train/id_train_split.txt')
    file_path.append('./dir_id_train/split_id_')
    split(init_list, file_path)


with open('./dir_id_train_anno/id_train_split_anno_.txt', 'r') as r:
    no_abs_list = [int(line.split('\t')[0]) for line in tqdm(r)]
no_abs_set = set(no_abs_list)
no_abs_list = list(no_abs_set)
no_abs_list.sort()
denominator = int(len(no_abs_list) / 3)

init_list = make_init_list(no_abs_list, denominator)

#print('spliting anno')
#split_anno(init_list)

print('spliting id')
split_id_train(init_list)
