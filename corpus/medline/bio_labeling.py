def preprocessing(sentence):
    sentence = sentence.replace(', ', ' , ')
    sentence = sentence.replace('. ', ' . ')
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
    #sentence = abs_sent[s_index:(ne_start_index - 1)]
    if e_index == 'end':
        sentence = abs_sent[s_index:]
    else:
        sentence = abs_sent[s_index:e_index]
    token_list = preprocessing(sentence)
    return token_list


def bio_labeling(abs_sent, start_index, ne, labeled_token_list, ne_no, last_ne_no):
    ne_start_index = int(ne[2])
    ne_end_index = int(ne[3])

    #NE以外のセンテンス処理
    o_token_list = o_token_processing(start_index, ne_start_index, abs_sent)
    labeled_token_list.extend(o_labeling(o_token_list))

    #NEの処理
    ne_token_list = preprocessing(abs_sent[ne_start_index:ne_end_index])
    labeled_token_list.extend(bi_labeling(ne_token_list))

    if ne_no == last_ne_no:
        #NE以外のセンテンス処理
        o_token_list = o_token_processing(ne_end_index, 'end', abs_sent)
        labeled_token_list.extend(o_labeling(o_token_list))
        return labeled_token_list, 0

    return labeled_token_list, ne_end_index


def o_labeling(token_list):
    return [token + ' O' for token in token_list]


def bi_labeling(token_list):
    for i, token in enumerate(token_list):
        if i == 0:
            string = token + ' B'
        else:
            string = token + ' I'
        labeled_token_list.append(string)
    return labeled_token_list


'''
l = "To further examine the transcriptional basis of this broad expression pattern, deletions in the 5' non-coding region of the gene were translationally fused to two promoterless reporter genes, encoding the enzymes chloramphenicol acetyl transferase (CAT) and beta-glucuronidase (GUS).\n"

l[213:228]
'chloramphenicol'
'''

with open('id_valid.txt', 'r') as r1, open('id_valid_anno_.txt', 'r') as r2:
    absts = [line.split('\t') for line in r1]
    annos = [line.strip('\n').split('\t') for line in r2]
    ne_abs_id_list = [int(i[0]) for i in annos]

for abs_id, abs_sent in absts:
    if judge(ne_abs_id_list, int(abs_id)):
        #This abst includes NE.
        ne_index_list = [i for i, ne_abs_id in enumerate(ne_abs_id_list) if ne_abs_id == int(abs_id)]
        '''
        abs_sent:
        They are N-acetylglucosamine pentasaccharides of which the non-reducing residue is N-methylated and N-acylated with cis-vaccenic acid (C18:1) or stearic acid (C18:0) and carries...  

        ne_index_list:
        [52, 53, 54]
        '''
        start_index = 0
        labeled_token_list = [] #ラベル付けされたセンテンスを格納するリスト
        last_ne_no = len(ne_index_list)
        for ne_no, ne_index in enumerate(ne_index_list):
            labeled_token_list, start_index = bio_labeling(abs_sent, start_index, annos[ne_index], labeled_token_list, ne_no, last_ne_no)
        print(labeled_token_list)
    else:
        #This abst does not include NE.
        print('No NE sentence')


'''
absts:
[['1', 'Primer extension and subsequent PCR amplification of these in vitro transcripts revealed gamma-thio-ATP-dependent, but no beta-thio-ATP-dependent, signals, although affinity labelling of overall in vitro transcripts still occurred with beta-thio-ATP.\n'], ['2', 'We conclude that the described plant nuclei reinitiated transcription non-specifically and that post-transcriptional transfer of the gamma-thio affinity label severely interfered with the detection of reinitiated transcripts..\n'], ['3', 'The location of gene expression of the Agrobacterium tumefaciens ipt gene promoter in transgenic tobacco plants was examined using the beta-glucuronidase (GUS) reporter gene.\n']]

annos:
[['6', 'Chloramphenicol', '213', '228'], ['10', 'NADP', '32', '36'], ['16', 'Amino Acids', '32', '43'], ['16', 'Ice', '108', '111'], ['16', 'Peptides', '173', '181']]
'''