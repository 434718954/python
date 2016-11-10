#-*- coding:utf-8 -*-

import re
import requests

class Spider:
#页面初始化
	def __init__(self):
		self.url = 'http://gz.meituan.com/category/meishi?mtt=1.index%2Ffloornew.nc.1.irj38puy'
		
	def get_class_index(self):
		r = requests.get(self.url)
		#print r.encoding
		#print r.text.encode('UTF-8')
		pattern1 = re.compile(r'<div class="label has-icon">分类：</div>(.*?)</div>',re.S)
		items = re.findall(pattern1,r.text.encode('UTF-8'))
		pattern2 = re.compile(r'<li.*?href="(.*?)">(.*?)</a></li>',re.S)
		items2 = re.findall(pattern2,items[0])
		f = open('mt_class_index.txt',"w+")
		llink=[]
		lname=[]
		lclass=[]
		for i in range(len(items2)):
			x,y=items2[i]
			llink.append(x)
			lname.append(y)
			lclass.append(str(i+1))
			f.write(str(i+1)+','+x+','+y+'\n')   
		f.close()
		result=zip(lclass,llink,lname)
		return result
		
	def getEverryClass(self,link):
		r = requests.get(link)
		pattern1 = re.compile(r'<div class="paginator-wrapper">(.*?)</div>',re.S)
		items = re.findall(pattern1,r.text.encode('UTF-8'))
		pattern2 = re.compile(r'<li.*?href="(.*?)".*?</li>',re.S)
		pattern3 = re.compile(r'<i class="icon icon-shangjia">.*?<a class="link f3 J-mtad-link".*?target="_blank">(.*?)</a>',re.S)#首页商家名称匹配
		items3 = re.findall(pattern3,r.text.encode('UTF-8'))
		if items:
			items2 = re.findall(pattern2,items[0]) #每一页的链接不含首页
			for i in range(len(items2)):
				curl ='http://gz.meituan.com'+items2[i]
				r1 = requests.get(curl)
				items4 = re.findall(pattern3,r1.text.encode('UTF-8'))
				items3+=items4
		return items3
	def savePageInfo(self):
		result=self.get_class_index()
		f1 = open('sj_names.txt',"w+")
		for i in range(len(result)):
			cl,lk,na =result[i]
			sjnames =self.getEverryClass(lk)
			for i in range(len(sjnames)):
				f1.write(cl+','+na+','+sjnames[i]+'\n')
		f1.close()
		
Spider().savePageInfo()

