from collections import Counter
import pandas
import requests
import json
import re
label_map = {
    0: "Negative",
    1: "Optimistic"
}

# 定义要提交的数据
datas = pandas.read_csv('data/hotel_xiecheng.csv')
data_list = datas['review'].tolist()
sentiment = []
# 构建请求的URL
url = "http://localhost:2345/sa"

# 发送POST请求
for data in data_list:
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
url = "http://localhost:2345/sa"
data = '["我第一次来监狱房 装修不错 很有风格 看着不错 网络速速的快 😎"]'
response = requests.post(url, data=data.encode('utf-8'))
text = json.loads(response.text)
label = label_map[text[0]['label']]
print(f"{text[0]['text']} : {label}")
'''