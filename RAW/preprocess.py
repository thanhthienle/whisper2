import os
import string
import json
import shutil
import random
random.seed(2023)


# Root
root = os.getcwd()
audio_path = os.path.join(root, "RAW/data/RAW/train/waves/RAWTRAIN")


# Kinda normalize
def remove_punctuations_and_spaces(text):
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = " ".join(text.split()).lower()
    text = text.replace('"', '')
    try:
        if text[-1] not in [".", "?", "!"]:
            text = text + "."
    except:
        pass
    return text


# Write list and writers
def write_obj(obj, writer, prefix=""):
    writer.write(prefix + obj["id"] + "\t" + remove_punctuations_and_spaces(obj["sentence"]) + "\n")

train_writer = open(os.path.join(root, "RAW/data/prompts-train.txt"), "w")
dev_writer = open(os.path.join(root, "RAW/data/prompts-dev.txt"), "w")
test_writer = open(os.path.join(root, "RAW/data/prompts-test.txt"), "w")

with open(os.path.join(root, "RAW/train.jsonl"), "r") as file:
    data = file.read().strip().split("\n")

train_count, dev_count, test_count = 0,0,0
for line in data:
    obj = json.loads(line)
    prob = random.uniform(0,1)
    if prob < 0.8:
        write_obj(obj, train_writer)
        train_count += 1
    elif prob < 0.9:
        original_path = os.path.join(audio_path, obj["id"] + ".wav")
        des_path = os.path.join(root, "RAW/data/RAW/dev/waves/RAWTEST", "_" + obj["id"] + ".wav")
        shutil.move(original_path, des_path)
        write_obj(obj, dev_writer, "_")
        dev_count += 1
    else:
        original_path = os.path.join(audio_path, obj["id"] + ".wav")
        des_path = os.path.join(root, "RAW/data/RAW/test/waves/RAWTEST", "_" + obj["id"] + ".wav")
        shutil.move(original_path, des_path)
        write_obj(obj, test_writer, "_")
        test_count += 1
