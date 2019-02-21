#数据库查询结果，用json返回
from sqlalchemy import create_engine
from pyecharts import Geo
import pandas as pd
import pymysql
import numpy as np
engine = create_engine("mysql+pymysql://root:wanli666@localhost:3306/stockdatabase?charset=utf8")
conn = pymysql.Connect(host='localhost', user='root', passwd='wanli666', db='stockdatabase', port=3306, charset='utf8')


def get_data_list():
    global pricelist,arealist
    #从数据库读取两张表的信息
    df1 = pd.read_sql('select * from test', con=conn)
    df3 = pd.read_sql('select * from try', con=conn)
    #只将‘价格’和‘市’提取
    prices0 = df1['价格']
    areas0 = df3['市']
    # 去重，将重复城市和价格一并去掉
    df4 = pd.concat([prices0, areas0], axis=1)
    data =df4.drop_duplicates(['市'])
    area1 = data['价格']
    price1 = data['市']
    # 用numpy处理，先将dataframe的列转化成数组，再将数组转化成列表
    area0 = np.array(price1)
    arealist = area0.tolist()
    price0 = np.array(area1)
    pricelist = price0.tolist()



#可视化部分，作出地图，显示数据
def test_geo():
    geo = Geo("大蒜价格和地区的关系", "", title_color="#fff",
              title_pos="center", width=1200,
              height=600, background_color='#404a59')
    attr=arealist
    value = pricelist

    geo.add("", attr, value, visual_range=[0, 15],visual_split_number=0.5, visual_text_color="#fff",
            symbol_size=16, is_visualmap=True)
    geo.show_config()
    geo.render('大蒜1.html')

# visual_range=[0, 20],,tooltip_formatter=geo_formatter,,geo_cities_coords=[0,0]

def main():
    # geo_formatter(params)
    get_data_list()
    test_geo()

if __name__ == "__main__":
    main()




