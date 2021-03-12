import jieba.analyse


def get_good_words():
    jieba.analyse.set_stop_words("./text_words/baidu_stopwords.txt")
    sentence = ''
    with open('./text_words/jieba_test', 'r', encoding='utf-8') as file:
        for line in file.readlines():
            if line == '\n':
                line = line.strip('\n')
            sentence += line
    print(sentence)
    res = jieba.analyse.textrank(sentence, topK=10, withWeight=True)
    print(res)
    return 0


if __name__ == '__main__':
    get_good_words()
