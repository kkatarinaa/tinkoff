#! python3

import argparse
import pickle
import model_class

class Generator():
    parser = argparse.ArgumentParser(description='Some info')
    parser.add_argument("-m", "--model")
    parser.add_argument("-p", "--prefix")
    parser.add_argument("-l", "--length", type=int)
    
    def __init__(self):
        args = Generator.parser.parse_args()
        with open(args.model, 'rb') as fin:
            model = pickle.load(fin)
        if not args.prefix:
            args.prefix = random.choice(model.frequency_dict.keys())[0]
        text = model.generate(args.prefix, args.length)
        with open("data/generated_text.txt", "w") as fout:
            fout.write(text)
        print(text)

Generator()
