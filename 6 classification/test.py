import requests
import csv

f = open('./data/review.csv', mode='a', encoding='utf-8-sig', newline='')
csv_write = csv.writer(f)
csv_write.writerow(['id', 'screen_name', 'text_raw', 'like_counts', 'total_number', 'created_at'])
# 请求头
headers = {
    # 用户身份信息
    'cookie': 'SINAGLOBAL=1395448135808.0483.1717214312876; ALF=1719808797; SUB=_2A25LXtZNDeRhGeNI7VEU9i_KyTuIHXVoEleFrDV8PUJbkNB-LWnBkW1NSFP-d3HUJabiAkDSiajlLiGjs87446fP; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWF92jFJJ4RVDaK7V2Zpvwx5JpX5KzhUgL.Fo-cSoefSo2ceoM2dJLoIXzLxKnLB-qLB-BLxKBLBonL12BLxKqL1heL122LxKBLB.2LB.2LxKqLB-BLB.zLxKBLBonL12BLxKBLB.eL1K2peK2t; XSRF-TOKEN=uEc_jZ1sUeXyN2hDeO2b6yZW; _s_tentry=weibo.com; Apache=9838532349851.836.1717310414254; ULV=1717310414257:2:2:1:9838532349851.836.1717310414254:1717214312890; WBPSESS=V6ISZtLsNeSFsvEHhAKzhR-fLPaA92m6Mbu9fLuOJXYyDmDh8AYUFbLG4ttEOKKPCig5fH4YCAig9EGWCrYhaUiopX8X1SB81l7Y7exBiJix_QLZ6tW7OHgeiV9H_WTQgN9nfOoEktZi2WINnQOwRA==',
    # 防盗链
    'referer': 'https://weibo.com/5352758859/Oh6aa1MHv',
    # 浏览器基本信息
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}


def get_next(next='count=10'):
    url = f'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id=5040752700425537&is_show_bulletin=3&is_mix=0&{next}&uid=5352758859&fetch_level=0&locale=zh-CN'

    response = requests.get(url=url, headers=headers)
    json_data = response.json()

    data_list = json_data['data']
    max_id = json_data['max_id']
    for data in data_list:
        text_raw = data['text_raw']
        id = data['id']
        created_at = data['created_at']
        like_counts = data['like_counts']
        total_number = data['total_number']
        screen_name = data['user']['screen_name']
        print(id, screen_name, text_raw, like_counts, total_number, created_at)

        csv_write.writerow([id, screen_name, text_raw, like_counts, total_number, created_at])

    max_str = 'max_id=' + str(max_id)
    get_next(max_str)


get_next()

