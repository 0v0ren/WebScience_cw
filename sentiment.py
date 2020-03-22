#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import os
import json


# clean data
def clean_text(text):
    """
    :func: remove the special signal
    :param string: string
    :return: cleaned string
    """
    # strings = re.sub(r"http(.)*?(\s|$)", "", t) # remove url link
    strings = text.replace('~', ' ').replace('!', ' ').replace('@', ' ').replace('#', ' ').replace('$', ' ') \
        .replace('%', ' ').replace('^', ' ').replace('&', ' ').replace('*', ' ').replace('(', ' ').replace(')', ' ') \
        .replace('-', ' ').replace('_', ' ').replace('+', ' ').replace('=', ' ').replace(':', ' ').replace(';', ' ') \
        .replace('"', ' ').replace('|', ' ').replace('/', ' ').replace('\\', ' ').replace('.', ' ').replace('<',' ').replace('>', ' ') \
        .replace('?', ' ').replace("\\", ' ').replace('？', ' ').replace('don\'t','do not').replace('\'ve',' have'),.replace('i\'m','i am')\
        .replace('\'re',' are').replace('\'ll',' will').replace('won\'t','will not').replace('haven\'t','have not')\
        .replace('hasn\'t','has not'),replace('isn\'t','is not'),replace('aren\'t','are not')\
               
    return ' '.join(set(strings.strip().split(' ')))  # set_word duplication


# Consecutive letters
def process_continue_word(word):
    """
    :param line_text: one line text, type: str
    :return: lower the letter, convert the shorthand to all-written
    """
    regex = re.compile(r"([a-zA-Z])(\1+)")
    return regex.sub(r"\1", word).lower()  # to lower letter


# Construct nrc dictionary
def process_nrc_dict(nrc_path):
    """
    :param nrc_path:nrc data path
    :return: example: [('anger', 'unfair', '1.02445030684195'), ('anger', 'unplug', '1.02445030684195'), ...]
    : what's more, replace # as '' because you had removed the # during the data-process step
    """
    word_sentiment_dict = {}
    with open(nrc_path, 'r', encoding='utf-8') as nrc_data:
        for lines in nrc_data.readlines():
            lines = lines.rstrip('\n').split('\t')
            word_sentiment_dict[lines[1].replace('#', '')] = lines[0]
    return word_sentiment_dict


# analysis
def text_sentiment_analysis(text_str, nrc_dict):
    result = []
    # sentiment_type = {"angry": "Anger", "excitement": "anticipation", "fear": "Fear", "happy": "joy", "disgust": "Fear"
    #     , "pleasant": 'trust', "surprise": "Surprise"}
    # sentiment_type = {"Anger": "angry", "anticipation": "excitement", "Fear": "fear", "joy": "happy"
    #     , 'trust': "pleasant", "Surprise": "surprise"}
    for word in list(text_str):
        senti = nrc_dict.get(word)
        result.append(senti)
    if len(result) and [i for i in result if i is not None]:
        return list(filter(None, result))[0]
    else:
        from collections import Counter
        # return 'trust'
        c = Counter(result)
        c_to_dict = dict(c)
        for key, value in c_to_dict.items():
            if value == max(c_to_dict.values()):
                res = str(value)
                return res


# Read emotion type
def read_emoji(emoji_path):
    emoj_list = []
    with open(emoji_path, 'r', encoding='utf-8') as ep:
        for line in ep.readlines():
            line = line.strip('\n')
            emoj_list.append(line)
    return emoj_list


if __name__ == '__main__':
    nrc_dictionary = process_nrc_dict('./NRC-Hashtag-Emotion-Lexicon-v0.2/NRC-Hashtag-Emotion-Lexicon-v0.2.txt')
    # print(nrc_dictionary)

    # pt = process_continue_word("AAAAAbbbbbcccc")
    # print(pt)

    # cleaned_str = clean_text('RT @LarAtLarian: Happy to see Pathfinder is doing so well - those are some impressive numbers.')
    # print(cleaned_str)
    sentiment_type = {"anger": "angry", "sadness": "excitement", "Fear": "fear", "joy": "happy", 'trust': "pleasant", "disgust": "surprise"}
    data_dir = './data/'
    result_dir = './result/'
    emoji_list = read_emoji('emoji.txt')
    data_name_list = os.listdir(data_dir)
    for data_name in data_name_list:
        with open(data_dir + data_name, 'r', encoding='utf-8') as dn:
            with open(result_dir + data_name.split('.')[0] + '_' + 'result.csv', 'w', encoding='utf-8') as dnw:
                for lines in dn:
                    temp_result_dict = {}
                    text_dict = json.loads(lines)
                    text_content = text_dict['text']
                    text_id = text_dict['_id'].get('$oid')
                    processed_text = ' '.join(
                        [process_continue_word(word) for word in clean_text(text_content).split(' ')])
                    # print(processed_text)
                    sentiment_classification = text_sentiment_analysis(processed_text, nrc_dictionary)
                    # print(sentiment_type)
                    temp_result_dict['id'] = text_id
                    temp_result_dict['raw_tweet'] = text_content
                    temp_result_dict['processed_tweet'] = processed_text
                    print(sentiment_classification)
                    temp_result_dict['label'] = sentiment_type.get(sentiment_classification)
                    dnw.write(json.dumps(temp_result_dict, ensure_ascii=False) + '\n')
