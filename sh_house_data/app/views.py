#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import codecs
from flask import Blueprint, render_template, request
import psycopg2

main = Blueprint('main', __name__)
name_encode = {}
distric_encode = {}
#反转字典
encode_name = {}
encode_distric = {}

def get_dict(filename,type):
    file = codecs.open(filename,'r','utf-8')
    data = file.readlines()
    file.close()
    if (type == 0):
        for cursor in data:
            cursor = cursor.strip().split(',')
            distric_encode.setdefault(cursor[0],cursor[1])
            encode_distric.setdefault(int(cursor[1]),cursor[0])
    else:
        for cursor in data:
            cursor = cursor.strip().split(',')
            name_encode.setdefault(cursor[0],cursor[1])
            encode_name.setdefault(int(cursor[1]),cursor[0])
    file.close()


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@main.route('/blocks', methods=['GET'])
def get_blocks():
    """
    获取小区信息
    :return:
    """

    street_val = request.values.get('street_val')

    blocks = [
        {'val': '贝越流明新苑', 'title': '贝越流明新苑'},
        {'val': '贝越流明新苑', 'title': '虹延小区'},
        {'val': '南文大厦', 'title': '南文大厦'},
        {'val': '斜土新村', 'title': '斜土新村'},
        {'val': '蒙西小区', 'title': '蒙西小区'},
        {'val': '士林华苑', 'title': '士林华苑'},
        {'val': '雅州公寓', 'title': '雅州公寓'},
        {'val': '金瓯万国大厦', 'title': '金瓯万国大厦'},
        {'val': '佳日公寓', 'title': '佳日公寓'},
    ]

    return json.dumps(blocks)


@main.route('/estimate', methods=['GET'])
def estimate():
    """
    根据参数预估结果接口
    :return:
    """
    #先构建一个编码字典
    get_dict('distric_encode_dict.txt',0)
    get_dict('name_encode_dict.txt',1)
    # 参数准备
    district_val = request.values.get('district_val')  # 区
    street_val = request.values.get('street_val')  # 街道
    block_val = request.values.get('block_val')  # 小区
    house_type_val = request.values.get('house_type_val')  # 户型
    floor_val = request.values.get('floor_val')  # 楼层
    built_val = request.values.get('built_val')  # 建成年份
    area_val = request.values.get('area_val') #面积
    conn = psycopg2.connect(database="test", user="postgres", password="postgres", host="127.0.0.1", port="5432")
    cursor = conn.cursor()
    #先把数据插到表中
    block_val_encode = name_encode[block_val]
    rooms = int(house_type_val[0]) + int(house_type_val[2])
    street_val_encode = distric_encode[street_val]
    #处理成数据库表要求的格式
    features = "{" + str(block_val_encode) + ',' + str(rooms) + ',' + str(area_val) + ',' + str(street_val_encode) + ',' + str(floor_val) + ',' + str(built_val) + "}"
    cursor.execute("insert into out_test VALUES (1,'%s',0)"%features)
    conn.commit()
    cursor.execute('''DROP TABLE IF EXISTS knn_result_regression''')
    conn.commit()
    cursor.execute('''SELECT * FROM madlib.knn('out_train','features','id','label','out_test','features','id',
    'knn_result_regression',5,True,'madlib.dist_norm2')''') #KNN，参数设置为5
    cursor.execute("SELECT * FROM knn_result_regression")
    row = cursor.fetchone()
    ids = row[3]#得到5个最相似的房子id
    #房子集合
    house_info_list = []
    for id in ids:
        cursor.execute("select * from out_train where id = (%d)"%id)
        house_info = cursor.fetchone()
        print('house_info: ',house_info)
        house_info_list.append(house_info)
    print(house_info_list)
    print('=============')
    print(house_info_list[0][1])
    print('-------------------')
    print(house_info_list[0][1][2])
    #删除插入的数据
    cursor.execute("delete from out_test")
    conn.commit()
    res = prepare_chart_data(house_info_list)
    conn.close()
    return json.dumps(res)


def prepare_chart_data(house_list):

    # 未选择小区
    if not house_list:
        x_data = ['小区一', '小区二', '小区三', '小区四', '小区五']
        legend = [{
            'name': '均价',
            'textStyle': {
                'color': '#2ea9ce',
            }
        }]
        series = [{
            'name': '均价',
            'type': 'bar',
            'data': ['3400000', '4400000', '2700000', '6000000', '5500600']
        }]
        tooltip = {
            '小区一': {
                'built_year': '1998',
            },
            '小区二': {
                'built_year': '2012',
            },
            '小区三': {
                'built_year': '2007',
            },
            '小区四': {
                'built_year': '1999',
            },
            '小区五': {
                'built_year': '2002',
            }
        }
    else:
        print('llll:...',house_list)
        print('*********************')
        print(encode_name[house_list[0][1][0]])
        price = [str(x[2]) for x in house_list]
        # x_data = [encode_name[house_list[0][1][0]],encode_name[house_list[1][1][0]],encode_name[house_list[2][1][0]],
        #           encode_name[house_list[3][1][0]],encode_name[house_list[4][1][0]]]
        x_data = ['房1', '房2', '房3', '房4', '房5']
        print(x_data)
        legend = [{
            'name': '房价/万元',
            'textStyle': {
                'color': '#2ea9ce',
            }
        }]
        series = [{
            'name': '房价',
            'type': 'bar',
            'data': price #['3400000', '4400000', '2700000', '6000000', '5500600']
        }]
        tooltip = {
            '房1': {
                'community_name':encode_name[house_list[0][1][0]],
                'room_num':str(house_list[0][1][1]),
                'area':str(house_list[0][1][2]),
                'district':encode_distric[house_list[0][1][3]],
                'floor':str(house_list[0][1][4]),
                'built_year':str(house_list[0][1][5]),
            },
            '房2': {
                'community_name':encode_name[house_list[1][1][0]],
                'room_num':str(house_list[1][1][1]),
                'area':str(house_list[1][1][2]),
                'district':encode_distric[house_list[1][1][3]],
                'floor':str(house_list[1][1][4]),
                'built_year':str(house_list[1][1][5]),
            },
            '房3': {
                'community_name':encode_name[house_list[2][1][0]],
                'room_num':str(house_list[2][1][1]),
                'area':str(house_list[2][1][2]),
                'district':encode_distric[house_list[2][1][3]],
                'floor':str(house_list[2][1][4]),
                'built_year': str(house_list[2][1][5]),
            },
            '房4': {
                'community_name':encode_name[house_list[3][1][0]],
                'room_num':str(house_list[3][1][1]),
                'area':str(house_list[3][1][2]),
                'district':encode_distric[house_list[3][1][3]],
                'floor':str(house_list[3][1][4]),
                'built_year': str(house_list[3][1][5]),
            },
            '房5': {
                'community_name':encode_name[house_list[4][1][0]],
                'room_num':str(house_list[4][1][1]),
                'area':str(house_list[4][1][2]),
                'district':encode_distric[house_list[4][1][3]],
                'floor':str(house_list[4][1][4]),
                'built_year':str(house_list[4][1][5]),
            },
        }

    res = dict(x_data=x_data, legend=legend, series=series, tooltip=tooltip, estimate_price=house_list[0][2])
    return res
