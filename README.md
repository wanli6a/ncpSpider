### 
>* 此项目是对全国商务部农产品商务信息公共服务平台（新农村商网）的部分农产品（生姜、大蒜）的信息的爬取（价格、地区）；通过selenium模拟浏览器进行操作（如实现自动搜索kEYWORDS"生姜"、"大蒜")，并利用相关解析库进行网页内容的爬取（价格地区信息表，其html将整个品类和价格、地区都放在了一张table里边）；
通过拼接URL来进行翻页，把每一页的信息都存储到了Mysql数据库，用jieba分词提取了“省市”关键字，利用pandas和dataframe进行了数据处理，形成了只含有地区和价格对应的json文件；
最后将json数据利用百度的开源Echarts实现了价格和地区关系的可视化。
>* （其实是去年五六月份的毕业设计的一部分，现在想起来github好久没用了，以后要多用，就也传上来记录一下。）
