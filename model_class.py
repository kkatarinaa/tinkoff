import argparse
import random
import pickle
import numpy as np


class Model:
    train_parser = argparse.ArgumentParser(description='Process info')
    train_parser.add_argument("-m", "--model", help="path to a file you want to download the model")
    train_parser.add_argument("-in", "--input_dir", help="path to texts")

    def __init__(self):
        args = Model.train_parser.parse_args()
        if not args.model:
            args.model = '.'
        if args.input_dir:
            with open(args.input_dir, 'r') as fin:
                text = fin.read()
        else:
            text = input()
        text = Model.tokened(text)
        self.frequency_dict = dict()
        for i in range(1, len(text)):
            self.add_in_dict(tuple([text[i - 1]],), text[i])
            if i >= 2:
                self.add_in_dict(tuple(text[i - 2:i]), text[i])
            if i >= 3:
                self.add_in_dict(tuple(text[i - 3:i]), text[i])
        self.add_probability()
        with open(args.model + '/model.pkl', 'wb') as fout:
            pickle.dump(self, fout)

    @staticmethod
    def tokened(s) -> list:
        res = ""
        s = s.lower()
        for i in range(len(s)):
            if not s[i].isalpha() and s[i] != ' ':
                res += ' '
            else:
                res += s[i]
        return res.split()

    def add_in_dict(self, key, word):
        if not key in self.frequency_dict:
            self.frequency_dict[key] = list()
        for pair in self.frequency_dict[key]:
            if word in pair:
                pair[1] += 1
                return
        self.frequency_dict[key].append([word, 1])

    def add_probability(self):
        for key in self.frequency_dict.keys():
            summ = 0
            for pair in self.frequency_dict[key]:
                summ += pair[1]
            for pair in self.frequency_dict[key]:
                pair[1] = pair[1] / summ

    def generate(self, prefix, length) -> str:
        result = [prefix.lower()]
        while len(result) != length:
            if len(result) == 1:
                result.append(self.next_word(tuple([result[-1]],)))
            elif len(result) == 2:
                result.append(self.next_word(tuple(result[-2:])))
            else:
                result.append(self.next_word(tuple(result[-3:])))
        return ' '.join(result)
        
    def next_word(self, last_words) -> str:
        possible_next = self.frequency_dict[last_words]
        only_words = [possible_next[i][0] for i in range(len(possible_next))]
        only_posibilities = [possible_next[i][1] for i in range(len(possible_next))]
        return np.random.choice(only_words, 1, only_posibilities)[0]
