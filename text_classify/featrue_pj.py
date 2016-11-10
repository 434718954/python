#-*- coding:utf-8 -*-
import jieba
import feature_selection as fs
from os.path import dirname 
from os.path import join
import re
import numpy as np 

class Feature_select:
#初始化
	def __init__(self,term_set_fs=None):
		self.term_set_dict=term_set_fs
		self.feature_selection_topn()
	
	def transform(self,doc_terms_list,term_dict=None):
		if term_dict:
			pass
		else:
			term_dict=self.term_set_dict
		term_class_df_mat = np.zeros((len(doc_terms_list),len(term_dict)), np.float32)
		for k in range(len(doc_terms_list)):
			for term in set(doc_terms_list[k]):
				term_index=term_dict.get(term)
				if term_index:
					term_class_df_mat[k][term_index]=1
		return term_class_df_mat
	def feature_selection_topn(self):
		
		#f = open("C:\\Users\\Administrator\\Desktop\\python note\\craw\\taobaomm\\sj_names.txt") 
		module_path = dirname(__file__)
		f = open(join(module_path, 'sj_names.txt'))
		class_list=[]
		term_str=[]
		try: 
			for line in f:  
				lt=line.split(',')
				if lt[1]=='全部':  #过滤掉全部分类
					continue
				class_list.append(lt[0])
				temstr=lt[2].split('（')
				seg_list = jieba.cut_for_search(temstr[0]) #搜索引擎模式
				terlist=", ".join(seg_list)  #解析成字符串
				try:
					term_str.append([term.strip() for term in terlist.split(',') if len(term.strip())>1]) #去掉空格字符转换为列表					
				except UnicodeEncodeError:
					print 'err'
		finally:
			f.close()
		print len(term_str)
		term_set_fs = fs.feature_selection(term_str, class_list, 'IG')[:2000]  #选取前1000个信息增益最大的词
		self.term_set_dict = dict(zip(term_set_fs, range(len(term_set_fs))))#生成字典
		f2 = open('feature_term_result.txt',"w+")
		for i in range(len(term_set_fs)):
			str =term_set_fs[i]
			f2.write(str.encode('utf-8')+'\n')
		f2.close()		
#		term_class_df_mat=self.transform(term_str,term_set_dict)



