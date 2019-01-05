import numpy as np
import matplotlib.pyplot as plt

'''
with open('loss.txt', 'r') as f:
    dev_f1 = [line.split()[14] for line in f]
with open('loss.txt', 'r') as f:
    test_f1 = [line.split()[24] for line in f]
print(dev_f1)
print(test_f1)
'''


class Score():

    def __init__(self, str_list):
        self.float_list = trans_float(str_list)
        self.epoch = list(range(len(self.float_list)))


def trans_float(str_list):
    float_list = [float(s) for s in str_list]
    return float_list


#baseline
base_dev_str_f1 = ['83.89', '88.02', '89.11', '90.62', '91.13', '91.89', '92.04', '92.64', '92.69', '92.98', '93.08', '92.96', '93.26', '93.78', '93.89', '93.79', '93.84', '93.80', '94.38', '94.50', '94.60', '94.73', '94.92', '94.77', '94.82']

base_test_str_f1 = ['38.31', '36.96', '36.44', '35.74', '33.55', '33.64', '34.14', '30.47', '31.93', '30.71', '31.67', '31.40', '30.75', '29.64', '28.69', '30.56', '29.86', '30.35', '28.16', '28.14', '28.27', '28.59', '26.75', '27.91', '27.75']

#tp
tp_dev_str_f1 = ['92.33', '95.24', '96.18', '96.44', '96.54', '97.03', '97.51', '97.31', '97.50', '97.61', '97.90', '97.81', '97.99', '97.95', '98.04', '97.97', '98.21', '98.12', '98.02', '98.14', '98.15', '98.38', '98.38', '98.47']

tp_test_str_f1 = ['40.71', '41.40', '37.52', '38.56', '39.00', '38.76', '37.11', '35.95', '36.45', '35.67', '34.08', '35.16', '33.88', '34.44', '33.71', '35.59', '33.39', '34.40', '33.84', '33.88', '34.45', '33.80', '33.70', '33.06']


base_dev = Score(base_dev_str_f1)
base_test = Score(base_test_str_f1)
tp_dev = Score(tp_dev_str_f1)
tp_test = Score(tp_test_str_f1)

max_axis = max([len(base_dev.epoch), len(base_test.epoch), len(tp_dev.epoch), len(tp_test.epoch)])

# red dashes, blue squares and green triangles
#plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
plt.plot(base_dev.epoch, base_dev.float_list, 'ro', label='base_dev')
plt.plot(base_test.epoch, base_test.float_list, 'bo', label='base_test')
plt.plot(tp_dev.epoch, tp_dev.float_list, 'rs', label='tp_dev')
plt.plot(tp_test.epoch, tp_test.float_list, 'bs', label='tp_test')

plt.axis([0, max_axis, 0, 100])
plt.xlabel('Epoch')
plt.ylabel('Span F1')
plt.legend()
plt.show()
