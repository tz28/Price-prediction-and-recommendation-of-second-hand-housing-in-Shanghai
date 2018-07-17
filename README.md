# Price-prediction-and-recommendation-of-second-hand-housing-in-Shanghai
Price prediction and recommendation of second-hand housing in Shanghai

Display the web program：

![系统展示](result.png)

1、This is project of the database course during my master study.

2、The main functions of the project is to crawl the second-hand housing data of LIANJIA in shanghai and evaluate the second-hand house price that user want to buy and recommand five of the most similar second-hand houses.

3、Development environment ：centos7 64bit、PostgreSQL9.5、MadLib1.13、pgAdmin4.2、Python2.7（web part）、python3.6（data crawling and preprocess）

**The web part were completed by wei jiang and the others were completed by me.**

----

**database_project：**

This part mainly completes the data crawling and data preprocessing:

crawler.py : crawl the second-hand house data in shanghai from LIANJIA  

preprocess.py : data preprocess

lianjia_data1.txt : the second-hand house data, a total of 42084 records. the examples as follows：

![数据展示](data_example.jpg)

lianjia_data2.csv : the same as lianjia_data1.txt

district_encode_dict.txt : the encode of region

name_encode_dict.txt : the encode of housing estate

tree_data.txt : data stored in PostgreSQL (meet The MADlib require format)

----

**sh_house_data：**

this is web part，the main function operation is in sh_house_data/app/views.py

----

**using MadLib to train the KNN model in PostgreSQL **

```SQL
DROP TABLE IF EXISTS knn_result_regression;
SELECT * FROM madlib.knn(
                'out_train',
                'features',
                'id',
                'label',
                'out_test',
                'features',
                'id',
                'knn_result_regression',
                 5, 
                True,
                'madlib.dist_norm2'
                );
```










