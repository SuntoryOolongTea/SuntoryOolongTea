import codecs
import re
import jieba.analyse
import math
import sys


# 去除文本内的空格、中文标点符号
def del_reg(filename):
    reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
    file_content = re.sub(reg, '', filename)
    return file_content


# 建立词袋模型，将中文词语降维成二维向量
def code(keyword, dictionary):
    array = [0] * len(dictionary)
    for content in keyword:
        array[dictionary[content]] += 1
    return array


# 通过计算两个向量的余弦距离来求文本相似度
def cos(vector1, vector2):
    vector_sum = 0
    fq1 = 0
    fq2 = 0
    for content in range(len(vector1)):
        vector_sum += vector1[content] * vector2[content]
        fq1 += pow(vector1[content], 2)
        fq2 += pow(vector2[content], 2)
    try:
        answer = round(float(vector_sum) / (math.sqrt(fq1) * math.sqrt(fq2)), 2)
    except ZeroDivisionError:
        answer = 0.0
    return answer


# encoding='utf-8'
file_path1 = sys.argv[1]
file_path2 = sys.argv[2]

try:
    file1 = codecs.open(file_path1, mode='r', encoding='utf-8').read()
    file2 = codecs.open(file_path2, mode='r', encoding='utf-8').read()
    file1 = del_reg(file1)
    file2 = del_reg(file2)
    # 提取文本里的关键词
    keyword1 = jieba.analyse.extract_tags(file1, topK=200, withWeight=False)
    keyword2 = jieba.analyse.extract_tags(file2, topK=200, withWeight=False)

    # 将文档1和文档2提取到的关键词合并成一个集合
    word_set = set(keyword1).union(set(keyword2))
    # 建立一个词典
    word_dict = dict()
    i = 0
    # 将两篇文章出现的关键词存入到字典里
    for word in word_set:
        word_dict[word] = i
        i += 1

    file1_code = code(keyword1, word_dict)
    file2_code = code(keyword2, word_dict)
    result = cos(file1_code, file2_code)
    output_path3 = sys.argv[3]
    # 将结果输入到所给路径的文件中
    file_answer = open(output_path3, 'w')
    file_answer.write(str(result))
    file_answer.close()
    print("查得重复率为：", result)
except IOError:
    print("文件不存在")