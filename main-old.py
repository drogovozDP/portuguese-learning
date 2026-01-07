import os
import re
import random
import argparse
from pathlib import Path


ROOT_DIR = Path(os.getcwd())


def collect_word_pairs(dict_name):
    regex_pattern = re.compile(r'#[^\n]*', re.MULTILINE)
    with open(ROOT_DIR / "dicts" / dict_name, "r") as fi:
        words = fi.read()
        words = [word.strip() for word in regex_pattern.sub('', words).splitlines() if word.strip() and word != "---"]

    def gen_sentences(pt_var):
        if len(pt_var) == 1 and len(pt_var[0]) == 1:
            return pt_var[0]
        if len(pt_var) == 0:
            return [""]
        new_pt_var = []
        for w in pt_var[0]:
            sentences = gen_sentences(pt_var[1:])
            for word in sentences:
                new_pt_var.append(f"{w} {word}")
        return new_pt_var

    word_pairs = []
    for word in words:
        pt, ru = word.split("|")
        pt_split, ru_split = pt.strip().split(" "), ru.strip().split(" ")
        pt_var, ru_var = [w.split("/") for w in pt_split], [w.split("/") for w in ru_split]
        pt_sentences, ru_sentences = gen_sentences(pt_var), gen_sentences(ru_var)
        word_pairs.append({
            "pt": pt_sentences,
            "ru": ru_sentences,
        })
    return word_pairs


def run(word_pairs):
    for word_pair in word_pairs:
        pt, ru = word_pair["pt"], word_pair["ru"]
        answer = input(f"{random.choice(ru)}:")
        if answer in pt:
            print("Correct!")
        else:
            print(f"Incorrect")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dict_name", help="A .txt file that contains portuguese words. If omitted, then all .txt files will be used.", default="")
    args = parser.parse_args()
    word_pairs = collect_word_pairs(args.dict_name)
    run(word_pairs)
