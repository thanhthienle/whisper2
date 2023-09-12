import random
import re


# Functions
PATTERN = r'\d+'
BASIC = {0: "không", 1: "một", 2: "hai", 3: "ba", 4: "bốn", 5: "năm", 6: "sáu", 7: "bảy", 8: "tám", 9: "chín", 10: "mười"}

def num_to_text(num: int):
    if num in BASIC:
        return BASIC[num]

    chuc = num // 10
    donvi = num % 10
    if chuc == 1:
        return "mười " + BASIC[donvi]
    else:
        first = BASIC[chuc]
        prob = random.uniform(0, 1)
        if prob < 0.5:
            middle = " "
        else:
            middle = " mươi "
        if donvi == 4:
            another_prob = random.uniform(0,1)
            if another_prob < 0.5:
                final = "bốn"
            else:
                final = "tư"
        elif donvi == 1:
            final = "mốt"
        elif donvi == 5:
          final = 'lăm'
        elif donvi == 0:
          if middle == ' mươi ':
            final = ''
            middel  = ' mươi'
          else:
            final = 'mươi'
        else: final = BASIC[donvi]
        return first + middle + final

def num_convert(sentence):
    sentence = sentence.replace("%", " phần trăm")
    match = re.finditer(PATTERN, sentence)
    lech = 0

    for something in match:
        start, end = something.span()
        word = sentence[start+lech:end+lech]
        num = int(word)
        text_num = num_to_text(num)
        sentence = sentence.replace(word, text_num, 1)
        lech += len(text_num) - len(word)

    return sentence

def remove_punctuations_and_spaces(text):
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = " ".join(text.split()).lower()
    text = text.replace('"', '')
    try:
        if text[-1] not in [".", "?", "!"]:
            text = text + "."
    except:
        pass
    return num_convert(text)

if __name__ == "__main__":
    for split in ["train", "dev", "test"]:
        with open(f"RAW/data/promtps-{split}.txt", "r") as file:
            data = file.read().strip().split("\n")
        writer = open(f"RAW/data/promtps-{split}.txt", "w")
        for line in data:
            id, transcript = line.split("\t")
            writer.write(id + "\t" + num_convert(transcript) + "\n")
