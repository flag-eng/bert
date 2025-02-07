# 准备工作：selenium,Chrome浏览器,ChromeDriver,pyquery 安装和配置
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
import csv
import time
import random
import os

# import pandas as pd
options = webdriver.ChromeOptions()
options.add_argument("disable-blink-features=AutomationControlled")  # 去掉webdriver痕迹
browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, 100)

###############参数设置############################
hotel_code = 1  #酒店起始编号
MAX_PAGE = 1000  #评论页上限
comment_page_nums = MAX_PAGE  #剩余需爬取页数
save_dir_csv = 'data'  # 保存文件夹
# save_dir_xlsx = 'data-beijing' # 保存文件夹
hotel_file = save_dir_csv + '/hotel_xiecheng.csv'


def index_page(url):
    '''
    打开初试页面，爬取第一页数据，然后进入后续页数爬取循环
    :param url: 初试页面链接
    :return: 无
    '''
    try:
        global comment_page_nums, browser
        browser.get(url)
        print(url)
        page = 1
        all = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.detail-headreview_all')))
        all.click()
        comment_page_nums = comment_page_nums - 1
        time.sleep(2)
        click_all = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-fastfilter button:first-child')))
        click_all.click()
        time.sleep(3)
        get_total_page()
        get_comment()
        time.sleep(2)
        while (comment_page_nums):
            comment_page_nums = comment_page_nums - 1
            page = page + 1
            next = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-pagination_item .forward')))
            next.click()
            time.sleep(random.randint(2, 4))
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.m-reviewCard-item')))
            wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.m_num_checked'), str(page)))
            get_comment()
            time.sleep(1)
    except TimeoutException as e:
        print(e.args)
    # finally:
    #     csv_to_xlsx_pd('/hotel_scores_xiecheng')


def get_total_page():
    '''
    获取评论总页数
    :return: 无
    '''
    global comment_page_nums
    html = browser.page_source
    doc = pq(html)
    page_bar = doc('.m-pagination_numbers div')
    nums = []
    for page in page_bar.items():
        num = page.text()
        nums.append(num)
    num = int(nums.pop())
    if num < comment_page_nums:
        comment_page_nums = num - 1
    print('此酒店共', num, '页评论！')


def get_comment():
    '''
    获取酒店评论
    :return: 无
    '''
    global hotel_code
    html = browser.page_source
    doc = pq(html)
    name = doc.find('.detail-headline_title h1').text()
    comment = {}
    comment_lists = doc('.m-tripReview .m-module-bg .list .m-reviewCard-item').items()
    for comment_list in comment_lists:
        comment = {
            "hotel_name": name,
            'id': comment_list.find('p.name').text(),
            'review': comment_list.find('.comment p').text()
        }
        save_comments(comment)


def save_comments(comment):
    '''
    保存酒店评论信息到 hotel_comments_H01.csv...
    :param comment: 酒店评论
    :return:
    '''
    with open(hotel_comment_file, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['hotel_name', 'id', 'review']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(comment)
        print(comment)


if __name__ == '__main__':
    # 遍历各个酒店id，爬取其网页上评论
    hotel_id = '107539299'
    hotel_code_encoded = str(hotel_code).rjust(2, '0')  # 酒店编码统一成两位数（100以内）
    file_name = '/hotel_comments_H{0}'.format(hotel_code_encoded)
    hotel_comment_file = hotel_file
    # 初始化各酒店评论保存文件
    with open(hotel_comment_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['hotel_name', 'id', 'review']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
    url = 'https://hotels.ctrip.com/hotels/' + hotel_id + '.html'
    index_page(url)
    comment_page_nums = MAX_PAGE
    browser.close()
