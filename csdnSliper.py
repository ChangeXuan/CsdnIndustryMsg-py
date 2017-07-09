# -*- coding:utf-8 -*-
import urllib 
import urllib2
import json
import re,os
import sys

class GetClass(object):
	def __init__(self):
		self.key = key
		self.header = {
			'Accept':'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
			'Accept-Encoding':'gzip, deflate',
			'Accept-Language':'zh-CN,zh;q=0.8',
			'Connection':'keep-alive',
			'Cookie':'uuid_tt_dd=2474288569045634660_20150824; __gads=ID=82723201032d3f46:T=1440386837:S=ALNI_MZZbjKZ7G4lbWDO6VWz8eYkN-3Lbw; csdn_cart_user_id=-472710767; _ga=GA1.2.163616098.1440386898; __utma=17226283.163616098.1440386898.1463360558.1463360642.8; lzstat_uv=212514760872053663|3506058@2939462@3590372@3525517@3603372@200@2819552@3610701@3434703@3491229@3612064@2671462@3609449@3560230; cache_user_quit=0; cache_cart_num=0; _JQCMT_ifcookie=1; _JQCMT_browser=6ec5c26dda1bd6ad2da99e2d2de24cc1; UN=ZeroSwift; UE="384638011@qq.com"; BT=1499315946673; dc_tos=osr0l2',
			'Host':'geek.csdn.net',
			'Referer':'http://geek.csdn.net/news',
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
			'X-Requested-With':'XMLHttpRequest',
		}

	# 抓取源数据
	def getSource(self,offset):
		url = 'http://geek.csdn.net/service/news/get_category_news_list?category_id=news&jsonpcallback=jQuery12349803693352853218_1499479917632&username=&from=%d&size=20&type=category&_=1499479917635'%offset
		try:
			request=urllib2.Request(url,headers = self.header)
			response=urllib2.urlopen(request)
			content=response.read()
		except Exception as e:
			content = None
			print('crawl data exception.'+str(e))
		return content

	# 取得内容
	def getContent(self,data):
		if data is None:
			return None
		for index,item in enumerate(data) :
			if item == "{":
				break
		data = data[index:-1]
		try:
			dataList = json.loads(data)['html']
			titleList = re.findall(' class="title" target="_blank">(.*?)</a>',dataList,re.S)
			urlList = re.findall('<a class="link_pjax" tabindex="0" href=(.*?) title=',dataList,re.S)
		except Exception as e:
			print('parse data exception.'+str(e))
		return [titleList,urlList]


	# 保存
	def save(self,titleList,urlList,saveFileName):
		if titleList is None or titleList is None:
			print 'save content params is None!'
			return
		saveData = []
		for index,title in enumerate(titleList):
			saveData.append(title+"--->"+urlList[index]+"\n\n")
		print saveData
		try:
			with open(saveFileName, 'a') as f:
				f.writelines([str(item) for item in saveData])
				f.close
			pass
		except Exception as e:
			print('save content exception.'+str(e))

	# 开始运行
	def run(self,endSet=20):
		offset = 0
		saveFile = './CSDN'
		saveFileName = saveFile+'/csdnTitle.txt'
		if os.path.exists(saveFileName):
			os.remove(saveFileName)
		else:
			os.makedirs(saveFile)
		while offset <= int(endSet):
			try:
				content = test.getSource(offset)
				[titleList,urlList] = test.getContent(content)
				test.save(titleList,urlList,saveFileName)
				pass
			except Exception, e:
				print "nonono"
				print e
			finally:
				offset += 20

if __name__ == "__main__" :
	test = GetClass()
	test.run(raw_input())
	pass
