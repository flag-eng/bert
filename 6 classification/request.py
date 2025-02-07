from collections import Counter
import pandas
import requests
import json
label_map = {
    0:"喜好",
    1:'高兴',
    2:'悲伤',
    3:"厌恶",
    4:'愤怒',
    5:'平和'
}
'''
# 定义要提交的数据
datas = pandas.read_csv('data/review.csv')
data_list = datas['text_raw'].tolist()
sentiment = []
# 构建请求的URL
url = "http://localhost:2345/sa"

# 发送POST请求
for data in data_list[1:]:
    data = data.replace('"', "")
    data = '["'+data+'"]'
    response = requests.post(url, data=data.encode('utf-8'))
    text = json.loads(response.text)
    label = label_map[text[0]['label']]
    sentiment.append(label)
    # 打印响应内容
    print(f"{text[0]['text']} : {label}")
count = Counter(sentiment)
print(count)
'''
data = '["啊啊啊啊啊啊啊啊啊啊烦死了"]'
url = "http://localhost:2345/sa"
response = requests.post(url, data=data.encode('utf-8'))
text = json.loads(response.text)
label = label_map[text[0]['label']]
print(f"{text[0]['text']} : {label}")

