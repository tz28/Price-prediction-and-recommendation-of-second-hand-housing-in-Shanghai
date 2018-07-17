#爬取链家网二手房的信息
import  requests as re
from bs4 import BeautifulSoup

citys = ['pudongxinqu','minhang','baoshan','xuhui','putuo','yangpu','changning','songjiang',
         'jiading','huangpu','jinan','zhabei','hongkou','qingpu','fengxian','jinshan','chongming']

def spider():
	urls = []
	for c in citys:
		url = 'http://sh.lianjia.com/ershoufang/%s/' %c
		response = re.get(url) #get 请求
		response = response.text.encode(response.encoding).decode('utf-8')
		soup = BeautifulSoup(response, 'html.parser')#对响应的链接源代码进行html解析
		"""
		使用finalAll方法，获取指定标签和属性下的内容,其实就是返回这一个div ==><div class="c-pagination">....</div>,返回一个长度为1的列表（列表内容为字符串）
		"""
		page = soup.findAll('div', {'class': 'c-pagination'})
		# print(len(page))
		# # print('======================')
		# print(page[0])
		# # print('======================')
		pages = [i.strip() for i in page[0].text.split('\n')]  # 抓取出每个区域的二手房链接中所有的页数
		# print(pages)
		#pages的形式为：['', '1', '2', '3', '4', '5', '6', '7', '', '...', '100', '下一页', '']
		#当就1页的时候为：['','1',''],只要大于1，为['','1','下一页',''],所以当列表长度大于3的时候取pages[-3]即为总页数，否则pages[-2]为总页数
		if len(pages) > 3:
			total_pages = int(pages[-3])
		else:
			total_pages = int(pages[-2])
		#拼接所有需要爬虫的链接
		for j in list(range(1, total_pages + 1)):
			urls.append('http://sh.lianjia.com/ershoufang/%s/d%s' % (c, j))
	file_txt = open('lianjia_data1.txt','a',encoding = 'utf-8')
	file_csv = open('lianjia_data2.csv', 'w', encoding='utf-8')
	file_txt.write('小区名字' + ',' + '户型' + ',' + '面积' + ',' + '地区' + ',' + '楼层' + ',' + '朝向' + ',' + '单价' + ',' + '总价' + ',' + '建成时间' + '\n')
	file_csv.write('小区名字' + ',' + '户型' + ',' + '面积' + ',' + '地区' + ',' + '楼层' + ',' + '朝向' + ',' + '单价' + ',' + '总价' + ',' + '建成时间' + '\n')
	for ur in urls:
		print('teee...' + ur)
		res = re.get(ur)
		res = res.text.encode(res.encoding).decode('utf-8')
		soup = BeautifulSoup(res, 'html.parser')
		page_items = soup.find('ul',{'class': 'js_fang_list'}).find_all('li')#每一页的房子list
		for li in page_items:  # 基于for循环，抓取出所需的各个字段信息
			title = li.find('a',{'class': 'text link-hover-green js_triggerGray js_fanglist_title'})['title'] # 每套二手房的标语，爬下来，但是没用到
			#name = item.find('a', {'class': 'laisuzhou'}).find('span')['title']  # 每套二手房的小区名称
			info = li.find('span', {'class': 'info-col row1-text'}).text.strip().split('|')  # 包括户型、面积、楼层、朝向
			room_type = info[0].strip()
			room_area = info[1].strip().rstrip('平')
			room_floor = info[2].strip()
			if(len(info) == 3):
				room_chaoxiang = ""
			else:
				room_chaoxiang = info[3].strip()
			info2 = li.find('span', {'class': 'info-col row2-text'}).text.strip().split('|')#包括小区名字、地理位置、建成时间
			name = info2[0].strip()
			region = info2[2].strip()
			if(len(info2) == 3):
				time = ""
			else:
				time = info2[3].strip().rstrip('年建')
			unit_price = li.find('span',{'class': 'info-col price-item minor'}).text.strip().rstrip('元/平').lstrip('单价')
			sum_price = li.find('span',{'class': 'total-price strong-num'}).text
			# print("==============")
			# print(title)
			# print("==============")
			print(name)
			# print(room_type)
			# print(room_area)
			# print(room_floor)
			# print(room_chaoxiang)
			# print('################################')
			# print(name)
			# print(region)
			# print(time)
			# print(unit_price)
			# print(sum_price)
			file_txt.write(name + ',' + room_type + ',' + room_area + ',' + region + ',' + room_floor + ',' + room_chaoxiang + ',' + unit_price + ','
			           + sum_price + ',' + time + '\n')
			file_csv.write(','.join((name, room_type, room_area, region, room_floor, room_chaoxiang, unit_price, sum_price, time)) + '\n')
	file_txt.close()
	file_csv.close()
if __name__ == '__main__':
	spider()