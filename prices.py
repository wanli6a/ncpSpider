from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import create_engine
import datetime as t
import time
import pandas as pd
import re
from requests.exceptions import RequestException
import requests
from chinese_province_city_area_mapper.transformer import CPCATransformer
import pymysql
from config import *
# from multiprocessing import Pool

engine = create_engine("mysql+pymysql://root:wanli666@localhost:3306/stockdatabase?charset=utf8")
conn = pymysql.Connect(host='localhost', user='root', passwd='wanli666', db='stockdatabase', port=3306,
                           charset='utf8')
chrome_options = Options()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)#
wait = WebDriverWait(browser, 10)
def search():
    #第一步先从首页跳转到价格查询，实现输入keywords并搜索——>跳转到keywords的价格行情页面
    try:
    #打开网页
        browser.get('http://nc.mofcom.gov.cn')
    #选择查询价格
        select = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
        "#header > div.header.w.clearfix > div.searchCol_01.fl.clearfix > div > div > div > span > em"))
        )
        select.click()
        #输入需要搜索的关键词比如“生姜”，搜索生姜
        sj = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
         "#header > div.header.w.clearfix > div.searchCol_01.fl.clearfix > div > div > ul > li:nth-child(2)")))
        sj.click()
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
            "#searchText")))
        input.send_keys(KEYWORD)
        see = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
        "#header > div.header.w.clearfix > div.searchCol_01.fl.clearfix > input")))
        see.click()
        now_url = browser.current_url#获取当前页面url即刚刚搜索完生姜的 页面的url
        new_url = now_url + '&startTime=' + str(get_startTime()) + '&endTime=' + str(get_endTime())
        html = get_page(new_url)
        get_page_number(html)
        for i in range(1, end_page + 1):
            next_url = new_url + '&page='+ str(i)
            browser.get(next_url)
            datas = pd.read_html(next_url)[0]
            global df
            df = pd.DataFrame(datas)
            # 删除不需要的走势、时间、产品名称这三列
            del df[4]
            del df[1]
            del df[0]
            df.drop(0, inplace=True)#删除第0行
            df.columns = ['价格', '市']#重新定义列名
            df.to_sql(name='test',con=engine,if_exists='append',index=False,index_label=False)
    except TimeoutException:
        return search()
#利用jieba分词提取市场信息中的城市名，以便在地图中显示
def get_city_name():
    cur = conn.cursor()
    cur.execute("select * from test")
    print('共有', cur.rowcount, '条数据')
    results = cur.fetchall()
    for r in results:
        location_str = [r[2]]
        cpca = CPCATransformer({"朝阳区": "北京市"})#遇到多个朝阳区则统一映射到北京市
        df2 = cpca.transform(location_str)
        df2.to_sql(name='try', con=engine, if_exists='append', index=False, index_label=False,)
    cur.close()

#用正则表达式从js中获取总页数，从而可以遍历爬取每一页，直到最后一页
def get_page_number(html):
    items = re.compile('<script>.*?\s.*?\s=\s(\d+);')
    page = re.search(items, html)
    global pageNumber
    pageNumber = page.group(1)
    print(pageNumber)
    global end_page
    end_page = int(pageNumber)
#判断当前页是否为当前页，若是，则返回状态码200，从而返回response.text（网页html文本信息）
def get_page(new_url):
    try:
        response = requests.get(new_url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None
#获取拼接url中的开始日期start_time和结束日期end_time
def get_endTime():
    TodayDate = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    return TodayDate
#获取结束日期即当前日期
def get_startTime():
    today =t.date.today()
    month = t.timedelta(days = 1)
    earlymonth = today-month
    return earlymonth
def main():
    search()
    get_city_name()
    browser.close()
    conn.close()


if __name__ == '__main__':
    main()



