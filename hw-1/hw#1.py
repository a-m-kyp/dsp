import re
import os
import sys
import argparse
import arabic_reshaper
from bidi.algorithm import get_display
from hazm import word_tokenize, POSTagger 
from utils import sub_alphabets

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)
valid_words = ["و", "صفر", "یک", "دو", "سه", "چهار", "پنج", "شش", "هفت", "هشت", "نه", "ده", "یازده", "دوازده", "سیزده", "چهارده", "پانزده", "شانزده", "هفده", "هجده",
               "نوزده", "بیست", "سی", "چهل", "پنجاه", "شصت", "هفتاد", "هشتاد", "نود", "صد", "دویست", "سیصد", "چهارصد", "پانصد", "ششصد", "هفتصد", "هشتصد", "نهصد", "هزار", "میلیون"]

phoneme = False

audio = {"yekan": {'0': "صفر",
                   '1': "یک",
                   '2': "دو",
                   '3': "سه",
                   '4': "چهار",
                   '5': "پنج",
                   '6': "شش",
                   '7': "هفت",
                   '8': "هشت",
                   '9': "نه"},
         "dahgan": {'10': "ده",
                    '11': "یازده",
                    '12': "دوازده",
                    '13': "سیزده",
                    '14': "چهارده",
                    '15': "پانزده",
                    '16': "شانزده",
                    '17': "هفده",
                    '18': "هجده",
                    '19': "نوزده",
                    '20': "بیست",
                    '30': "سی",
                    '40': "چهل",
                    '50': "پنجاه",
                    '60': "شصت",
                    '70': "هفتاد",
                    '80': "هشتاد",
                    '90': "نود"},
         "sadgan": {'100': "یکصد",
                    '200': "دویست",
                    '300': "سیصد",
                    '400': "چهارصد",
                    '500': "پانصد",
                    '600': "ششصد",
                    '700': "هفتصد",
                    '800': "هشتصد",
                    '900': "نهصد"}}

file_name = {'0': "صفر",
        '1': "یک",
        '2': "دو",
        '3': "سه",
        '4': "چهار",
        '5': "پنج",
        '6': "شش",
        '7': "هفت",
        '8': "هشت",
        '9': "نه",
        '10': "ده",
        '11': "یازده",
        '12': "دوازده",
        '13': "سیزده",
        '14': "چهارده",
        '15': "پانزده",
        '16': "شانزده",
        '17': "هفده",
        '18': "هجده",
        '19': "نوزده",
        '20': "بیست",
        '30': "سی",
        '40': "چهل",
        '50': "پنجاه",
        '60': "شصت",
        '70': "هفتاد",
        '80': "هشتاد",
        '90': "نود",
        '100': "یکصد",
        '200': "دویست",
        '300': "سیصد",
        '400': "چهارصد",
        '500': "پانصد",
        '600': "ششصد",
        '700': "هفتصد",
        '800': "هشتصد",
        '900': "نهصد",
        "1000": "هزار",
        "1000000": "میلیون",
        "1000000000": "میلیارد",
        # 'O': "[cls]",
        'O': "cls",
        'e': "e",
        'daneshgah': "دانشگاه",
        'tehran': "تهران",
        'be': "به",
        'koja': "کجا",
        'chenin': "چنین",
        'shetaban': "شتابان",
        'amir': "امیر",
        'mohammad': "محمد",
        'kouyesh': "کویش",
        'pour': "پور",
        'silence': "silence",
        'i': "ای",
        'u': "او",
        'AAAA': "آ",
        'p': "پ",
        'b': "ب",
        't': "ت",
        'd': "د",
        'k': "ک",
        'g': "گ",
        'q': "ق",
        ']': "ژ",
        '$': "چ",
        ',': "ج",
        'f': "ف",
        'v': "و",
        's': "س",
        'z': "ز",
        '.': "ش",
        '[': "ژ",
        'x': "خ",
        'h': "ه",
        'l': "ل",
        'r': "ر",
        'm': "م",
        'n': "ن",
        'y': "ی",
}

place_dict = {
    'هزار': 'hezar',
    'میلیون': 'milion',
    'میلیارد': 'milion'
}

place_values = {'0': "یکان", '1': "هزار", '2': "میلیون", '3': "میلیارد", '4': "tenthousands", '5': "hundredthousands", '6': "millions", '7': "tenmillions", '8': "hundredmillions",
                '9': "billions", '10': "tenbillions", '000000000000': "hundredbillions", '0000000000000': "trillions", '00000000000000': "tentillions", '000000000000000': "hundredtrillions"}

##########################################################
##################  Arguments Parser #####################
##########################################################
parser = argparse.ArgumentParser()

parser.add_argument("--number", help="Enter a number")
parser.add_argument("--persian_number", help="Enter a sentence")
parser.add_argument("--persian_sentence", help="Enter a sentence")

parser.add_argument("--number_phoneme", help="Enter a number")
parser.add_argument("--persian_number_phoneme", help="Enter a sentence")
parser.add_argument("--persian_sentence_phoneme", help="Enter a sentence")

args = parser.parse_args()
args = vars(args)



def rtl_convert(text):
    reshaped_text = arabic_reshaper.reshape(text)
    converted = get_display(reshaped_text)
    return converted

for i in range(len(valid_words)):
    valid_words[i] = rtl_convert(valid_words[i])

def normalize_persian_number(sentence):
    """
        check for valid words else exiting the program
    """
    valid_word_flag = False
    for word in sentence.split():
        if word not in valid_words:
            valid_word_flag = True
            break
    if valid_word_flag:
        print("\033[1;31m" + "Error: You must enter valid words" + "\033[0m")
        sys.exit()
    return sentence

def normalize_number(number):
    """
        normalize arabic number to english
    """
    arabic_to_english_number_dict = {
        '۰': '0',
        '۱': '1',
        '۲': '2',
        '۳': '3',
        '۴': '4',
        '۵': '5',
        '۶': '6',
        '۷': '7',
        '۸': '8',
        '۹': '9',
    }

    for arabic_number, english_number in arabic_to_english_number_dict.items():
        number = number.replace(arabic_number, english_number)
    return number

def normalize_persian_sentence(sentence):
    print("\033[1;31m" + "You Entered: " + "\033[0m" + sentence)
    if sentence is not None and sentence != "":
        # if sentence contains digits then exit
        if any(char.isdigit() for char in sentence):
            print("\033[1;31m" + "Error: You must enter a sentence" + "\033[0m")
            sys.exit()
        else:
            # use hazm to specify POS of words
            tagger = POSTagger(model='resources/postagger.model')
            word_tag = tagger.tag(word_tokenize(sentence))
            words = []
            for word, tag in word_tag:
                if tag == "Ne":
                    # add e to list of words
                    words.append(word)
                    words.append("[e]")
                else:
                    words.append(word)
    return words

def check_input(args):

    global file_type, arguments, phoneme

    if args["number"] and args["persian_number"] and args["persian_sentence"] and args["persian_number_phoneme"] and args["persian_sentence_phoneme"]:
        print("\033[1;31m" + "Error: You must enter only one option" + "\033[0m")
        sys.exit()

    elif args["persian_number"] or args["persian_number_phoneme"]:
        arguments = args["persian_number"] or args["persian_number_phoneme"]
        persian_number_value = args["persian_number"] or args["persian_number_phoneme"]

        if args["persian_number_phoneme"]:
            phoneme = True
            file_type = "phoneme"
        else:
            file_type = "number"

        return process_sentence(normalize_persian_number(rtl_convert(persian_number_value)))

    elif args["number"] or args["number_phoneme"]:
        arguments = args["number"] or args["number_phoneme"]
        number_value = args["number"] or args["number_phoneme"]

        if args["number_phoneme"]:
            phoneme = True
            file_type = "phoneme"
        else:
            file_type = "number"
        arguments = "number"

        if re.match(r'^[0-9]+$', args["number"]):
            return process_number(args["number"])
        elif re.match(r'^[۰-۹]+$', args["number"]):
            return process_number(normalize_number(args["number"]))
        else:
            print("\033[1;31m" +
                  "Error: You can't enter this number" + "\033[0m")
            sys.exit()
    elif args["persian_sentence"]:
        file_type = "word"
        arguments = "persian_sentence"
        return process_persian_sentence(normalize_persian_sentence(args["persian_sentence"]))

    elif args["persian_sentence_phoneme"]:
        file_type = "phoneme"
        arguments = "persian_sentence_phoneme"
        return process_persian_sentence_phoneme(normalize_persian_sentence(args["persian_sentence_phoneme"]))

    else:
        print(
            "\033[1;31m" + "Error: You must enter either --persian_sentence or --number or --persian_number" + "\033[0m")
        sys.exit()

def intersperse(lst, sep):
    """ #### Insert a separator between every two adjacent items of the list.
        Input list and separator
        return list with separator between every two adjacent items
    """
    result = [sep] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result

def process_sentence(sentence):
    print("\033[1;32m" + "You entered: " + "\033[0m", sentence)
    words = sentence.split(" ﻭ ")
    words = intersperse(words, "[cls]")
    result = []
    place_dict_keys = [rtl_convert(place_dict_key)
                       for place_dict_key in list(place_dict.keys())]
    for element in words:
        if any(place in element for place in place_dict_keys):
            key = [place for place in place_dict_keys if place in element][0]
            temp_element = element.replace(key, '').replace(' ', '')
            result.append(key)
            result.append(temp_element)
        else:
            result.append(element)
    if phoneme:
        return process_persian_sentence_phoneme(apply_to_phoneme(result))
    return generate_order(result[::-1])

def convert_to_3_digits(number):
    """ #### convert enetered number to 3 digits chunks
        Input number
        return list of 3 digits chunks
    """
    number = str(number)
    number = number[::-1]
    number_list = []
    for i in range(0, len(number), 3):
        number_list.append(number[i:i+3][::-1])
    return number_list

def get_place_notation(number):
    """ #### get place notation of a number
    """
    place_notation = []
    for i in range(len(number)):
        place_notation.append(place_values[str(i)])
    return place_notation

def process_order(chunk):
    sound_name = []
    str_list = ['sadgan', 'dahgan', 'yekan']

    if len(chunk) == 1:
        sound_name.append(audio[str_list[2]][chunk])
    elif len(chunk) == 2:
        if chunk[0] == '1':
            sound_name.append(audio[str_list[1]][chunk[0]+chunk[1]])
        elif chunk[1] == '0':
            sound_name.append(audio[str_list[1]][chunk[0]+'0'])
        else:
            sound_name.append(audio[str_list[1]][chunk[0]+'0'])
            sound_name.append(audio[str_list[2]][chunk[1]])

    elif len(chunk) == 3:
        if chunk[0] == '0' and chunk[1] == '0' and chunk[2] == '0':
            pass

        elif chunk[0] != '0' and chunk[1] == '0' and chunk[2] == '0':
            sound_name.append(audio[str_list[0]][chunk[0]+'00'])

        elif chunk[0] == '0' and chunk[1] != '0' and chunk[2] != '0':
            sound_name.append(audio[str_list[1]][chunk[1]+'0'])
            sound_name.append(audio[str_list[2]][chunk[2]])

        elif chunk[0] == '0' and chunk[1] != '0' and chunk[2] == '0':
            sound_name.append(audio[str_list[1]][chunk[1]+'0'])

        elif chunk[0] != '0' and chunk[1] == '0' and chunk[2] != '0':
            sound_name.append(audio[str_list[0]][chunk[0]+'00'])
            sound_name.append(audio[str_list[2]][chunk[2]])

        elif chunk[1] == '1' and chunk[0] != '0' and chunk[2] != '0':
            sound_name.append(audio[str_list[0]][chunk[0]+'00'])
            dahgan = chunk[1] + chunk[2]
            sound_name.append(audio[str_list[1]][dahgan])

        elif chunk[2] == '0' and chunk[0] != '0' and chunk[1] != '0':
            sound_name.append(audio[str_list[0]][chunk[0]+'00'])
            sound_name.append(audio[str_list[1]][chunk[1]+'0'])

        else:
            sound_name.append(audio[str_list[0]][chunk[0]+'00'])
            sound_name.append(audio[str_list[1]][chunk[1]+'0'])
            sound_name.append(audio[str_list[2]][chunk[2]])
    return sound_name

def generate_order(result_list):
    print("====================== generate_oder =======================")

    if not phoneme:
        temp_dict = {}
        for key, value in file_name.items():
            temp_dict[key] = rtl_convert(value)
        print(temp_dict)

    order = []
    print(result_list)
    for audio in result_list:
        print("\033[1;32m" + audio + "\033[0m")
        if audio == '[cls]' or audio == 'cls':
            order.append("O.wav")
        elif audio == 'ا':
            order.append("a.wav")
        elif audio == 'اِ':
            order.append("e.wav")
        elif audio in ['ت', 'ط']:
            order.append("t.wav")
        elif audio in ['ق', 'غ']:
            order.append("q.wav")
        elif audio in ['ؤ', 'أ', 'ع']:
            order.append("].wav")
        elif audio in ['س', 'ث', 'ص']:
            order.append("s.wav")
        elif audio in ['ز', 'ذ', 'ظ', 'ض']:
            order.append("z.wav")
        elif audio in ['ه', 'ح']:
            order.append("h.wav")
        else:
            if phoneme:
                keys = [key for key, value in file_name.items() if value == audio]
                print("\033[1;32m keys:  \033[0m", keys)
                order.append(keys[0]+".wav")
            else:
            keys = [key for key, value in temp_dict.items() if value == audio]
            print("\033[1;32m keys:  \033[0m", keys)
            order.append(keys[0]+".wav")
    return order

def generate_audio_order(chunked, units):
    audio_order = []
    for chunk, unit in zip(chunked, units):
        audio_order.append(process_order(chunk))
        # expand last element of audio_order with unit
        if unit != 'یکان':
            audio_order[-1].append(unit)
    return audio_order

def add_cls_each_chunk_sentence(audio_order):
    """
        if there is an element after this element add a 'cls' 
    """
    num = 0
    temp_audio_order = []
    for chunk in audio_order:
        iterator = 0
        for word in chunk:
            if word != chunk[-1]:
                if not any(key in chunk[iterator+1] for key in place_dict.keys()):
                    temp_audio_order.append(word)
                    temp_audio_order.append('cls')
                else:
                    temp_audio_order.append(word)
            else:
                temp_audio_order.append(word)
            iterator += 1
        audio_order[num] = temp_audio_order
        num += 1
        temp_audio_order = []

    temp_audio_order = []
    for chunk in audio_order:
        if chunk != audio_order[-1]:
            temp_audio_order.append(chunk)
            temp_audio_order.append(['cls'])
        else:
            temp_audio_order.append(chunk)
    return temp_audio_order

def process_number(number):
    print("\033[1;32m" + "You entered: " + "\033[0m", number)
    number = number.replace(' ', '')
    chunked = convert_to_3_digits(number)[::-1]
    units = get_place_notation(chunked)[::-1]

    generated_order = generate_audio_order(chunked, units)
    result = add_cls_each_chunk_sentence(generated_order)
    temp_result = []
    for element in result:
        if len(element) >= 1 and not (element[0] == element[-1] and element[0] == 'cls'):
            temp_result.append(element)
    semi_result = []
    result = []
    for element in temp_result:
        for word in element:
            if word in place_dict.keys() and len(element) == 1:
                pass
            else:
                semi_result.append(word)
        if semi_result != []:
            result.append(semi_result)
        semi_result = []
    result = intersperse(result, ['cls'])
    result =  [rtl_convert(item) for element in result for item in element]
    if phoneme:
        return process_persian_sentence_phoneme(apply_to_phoneme(result))
    return generate_order(result)

def apply_to_phoneme(result_list):
        temp_result = []
        for element in result_list:
            print(element)
            if element == 'cls' or element == "[cls]":
                temp_result.append('cls')
            elif element == 'silence':
                temp_result.append('silence')
            else:
                temp_result.append(list(element)[::-1])
        return temp_result

# word
def process_persian_sentence(sentence):
    temp_sentence = []
    for word in sentence:
            if word != '[e]':
                temp_sentence.append(rtl_convert(word))
            else:
                temp_sentence.append('e')
                temp_sentence.append('silence')
    if phoneme:
        return process_persian_sentence_phoneme(apply_to_phoneme(temp_sentence))
    return generate_order(temp_sentence)

# phoneme
def process_persian_sentence_phoneme(sentence):
    temp_sentence = []
    for word in sentence:
        for char in word:
            if char != '[' and char != ']':
                if char != 'e':
                    temp_sentence.append(char)
                else:
                    temp_sentence.append('e')
                    temp_sentence.append('silence')
    return generate_order(temp_sentence)

if __name__ == "__main__":
    result = check_input(args)
    print("\033[1;31m" + "Result: " + "\033[0m", result)
    for index, element in enumerate(result):
        print("index = ", index, "element = ", element)

    if phoneme:
        print(arguments)
        result = [ 'assets/%s/' %(file_type) + element for element in result]
        output_name =  '_'.join(arguments.split(' ')) + '_phoneme' + '.wav'
    else:
        result = [ 'assets/%s/' %(file_type) + element for element in result]
        output_name =  '_'.join(arguments.split(' ')) + '.wav'

    print(file_type)
    command = 'sox %s %s' % (' '.join(result), output_name)
    os.system(command)
    if os.path.isfile(output_name):
        print("\033[1;32m" + "Successfully generated: " + "\033[0m", output_name)
    else:
        print("\033[1;31m" + "Failed to generate: " + "\033[0m", output_name)
    sys.exit()