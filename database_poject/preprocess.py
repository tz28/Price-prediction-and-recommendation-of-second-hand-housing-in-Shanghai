import re
from datetime import datetime
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

#处理建成年代缺失值
def del_miss_value():
	file = open('lianjia_data1.txt',encoding='utf-8')
	data = file.readlines()[1:]#去掉表头
	file.close()
	file = open('lianjia.txt','a',encoding='utf-8')
	for cursor in data:
		cursor1 = cursor.strip().split(',')
		if cursor1[8] != "":
			file.write(cursor)
	file.close()

#处理特征(房间数、楼层、房屋年龄)形成训练集
def process_features():
	file = open('lianjia.txt')
	data = file.readlines()
	file.close()
	file = open('lianjia1.txt', 'a', encoding='utf-8')
	for cursor in data:
		cursor = cursor.strip().split(',')
		rooms = int(cursor[1][0]) + int(cursor[1][2])
		floor = re.sub('\D','',cursor[4])#正则表达式提取数字
		room_age = datetime.now().year - int(cursor[8])
		file.write(cursor[0] + ',' + str(rooms) + ',' + cursor[2] + ',' + cursor[3] + ',' + floor + ',' + cursor[6] + ','
		           + cursor[7] + ',' + str(room_age) + '\n')
	file.close()

#对小区地区进行索引编码
def feature_encode():
	data = pd.read_csv('lianjia1.txt', sep=',', encoding='utf-8',
	                   names=['name', 'rooms', 'area', 'district', 'floor', 'uprice', 'sprice', 'age'])
	#对小区索引编码
	name_list = list(data['name'])
	arr_name = LabelEncoder().fit_transform(data['name'])
	data['name'] = arr_name
	file = open('name_encode_dict.txt', 'a', encoding='utf-8')
	for i in range(len(name_list)):
		file.write(name_list[i] + ',' + str(arr_name[i]) + '\n')
	file.close()
	# district_list = list(data['district'])
	arr_district = LabelEncoder().fit_transform(data['district'])
	data['district'] = arr_district
	# file = open('distric_encode_dict.txt','a',encoding='utf-8')
	# for i in range(len(district_list)):
	# 	file.write(district_list[i] + ',' + str(arr_district [i]) + '\n')
	# file.close()
	data.to_csv('lianjia3.txt', index=False, sep=',', header=False)
#对特征正则化

#把特征组合成结构体的形式，因为postgresql中的madlib要求这种形式
def combine_featurs():
	file = open('lianjia3.txt', encoding='utf-8')
	data = file.readlines()[1:]  # 去掉表头
	file.close()
	file = open('train_data.txt','a',encoding='utf-8')
	for cursor in data:
		cursor = cursor.strip().split(',')
		features = '{' + str(cursor[0]) + ',' + str(cursor[1]) + ',' + str(cursor[2]) + ',' + str(cursor[3]) + ',' + str(cursor[4]) + ',' + cursor[7] + '}'
		label = cursor[6]
		file.write(features + '#' + label + '\n')
	file.close()

#去除数据集中冗余的样本
def remove_redundancy():
	file = open('lianjia3.txt', encoding='utf-8')
	data = file.readlines()
	file.close()
	file = open('no_redundancy_lianjia3.txt', 'a', encoding='utf-8')
	lis = []
	for cursor in data:
		cursor = cursor.strip()
		if cursor not in lis:
			lis.append(cursor)
			file.write(cursor + '\n')
	file.close()

#删除uprice
def del_feature():
	file = open('no_redundancy_lianjia3.txt', encoding='utf-8')
	data = file.readlines()[1:] #去掉表头
	file.close()
	file = open('tree_data.txt', 'a', encoding='utf-8')
	for cursor in data:
		cursor = cursor.strip().split(',')
		file.write(str(cursor[0]) + ',' + str(cursor[1]) + ',' + str(cursor[2]) + ',' + str(cursor[3]) + ',' + str(cursor[4]) + ',' + str(cursor[7]) + ',' + str(cursor[6]) + '\n')
	file.close()



if __name__ == '__main__':
	#del_miss_value()
	# process_features()
	#feature_encode()
	#combine_featurs()
	#remove_redundancy()
	del_feature()