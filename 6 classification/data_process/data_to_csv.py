import json
import pandas as pd
from collections import Counter

label_map = {
    "Null": 0,
    "Like": 1,
    'Sad': 2,
    "Disgust": 3,
    'Anger': 4,
    'Happiness':5
}

sentiment = []
review = []
with open('./data/train.json', 'r',encoding='utf-8') as f:
    data = json.load(f)
    for se in data:
        label = se[1]
        view = se[0].strip()
        view = view.replace(" ","")
        view = view.replace('"',"")
        #label = label_map[label]
        sentiment.append(label)
        review.append(view.replace(',', '，'))

save = pd.DataFrame({'label': sentiment, 'review': review})
save.to_csv('data/train.csv', index=False, sep=',')
count = Counter(sentiment)
print(count)
