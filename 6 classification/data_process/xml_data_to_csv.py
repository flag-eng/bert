import random
import xml.etree.ElementTree as ET

from collections import defaultdict
import pandas as pd
from collections import Counter
label_map_en = {
    "like": 0,
    'happiness':1,
    'sadness': 2,
    "disgust": 3,
    'anger': 4
}
label_map_cn = {
    "喜好": 0,
    '高兴':1,
    '悲伤': 2,
    "厌恶": 3,
    '愤怒': 4
}
label_map = {
    "Smooth": 0,
    "Like": 1,
    'Sad': 2,
    "Disgust": 3,
    'Anger': 4,
    'Happiness':5
}

change = {
    1:0,
    2:2,
    3:3,
    4:4,
    5:1,
    0:5
}
label_xlsx = {
    'angry':4,
    'neutral':5,
    'happy':1,
    'sad':2
}
sentiment = []
review = []
# 提取评论内容和情感分类
def extract_data(tree,type):
    root = tree.getroot()
    for sentence in root.findall('.//sentence'):
        opinionated = sentence.get('opinionated')
        emotion1_type = sentence.get('emotion-1-type')
        if opinionated == "Y" and emotion1_type != "" and emotion1_type != "none"\
                and emotion1_type != "恐惧" and emotion1_type != "惊讶" and emotion1_type != "surprise"\
                and emotion1_type != "fear" and emotion1_type != "None":
            comment = sentence.text
            if type == 1:
                label = label_map_en[emotion1_type]
            elif type == 2:
                label = label_map_cn[emotion1_type]
            sentiment.append(label)
            review.append(comment)

# 解析XML文件
tree = ET.parse('../data/nlpcc2013.xml')
extract_data(tree,2)
tree = ET.parse('../data/nlpcc2014_1.xml')
extract_data(tree,1)
tree = ET.parse('../data/nlpcc2014_2.xml')
extract_data(tree,1)

datas = pd.read_csv('../data/train.csv')
label_list = datas['label'].tolist()
stc_list = datas['review'].tolist()
for label, comment in zip(label_list, stc_list):
    ch_label = change[label]
    sentiment.append(ch_label)
    review.append(comment)

#save = pd.DataFrame({'label': sentiment, 'review': review})
#save.to_csv('../data/nlpcc.csv', index=False, sep=',')


df = pd.read_excel('../data/usual_train.xlsx')
# 获取活动工作表（通常是第一个工作表）
# 读取单元格数据
lebel = df['情绪标签'].values
sen = df['文本'].values
for label, comment in zip(lebel, sen):
    if label != 'fear' and label != 'surprise':
        ch_label = label_xlsx[label]
        sentiment.append(ch_label)
        review.append(comment)
count = Counter(sentiment)
print(count)


# 创建一个字典，用于按标签分类存储评论
label_to_comments = defaultdict(list)
for l, c in zip(sentiment, review):
    label_to_comments[l].append(c)

# 找到最小的分类数量
min_count = min(len(comments) for comments in label_to_comments.values())

# 对每个分类进行删减
balanced_sentiment = []
balanced_review = []
for label, comments in label_to_comments.items():
    random.shuffle(comments)  # 随机打乱评论顺序
    balanced_sentiment.extend([label] * min_count)
    balanced_review.extend(comments[:min_count])

count = Counter(balanced_sentiment)
print(count)
save = pd.DataFrame({'label': balanced_sentiment, 'review': balanced_review})
save.to_csv('../data/new_data.csv', index=False, sep=',')


