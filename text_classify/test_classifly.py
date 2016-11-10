#-*- coding:utf-8 -*-
import jieba
import featrue_pj as fj
from os.path import dirname 
from os.path import join
from sklearn.cross_validation import   train_test_split  #k折交叉模块  
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
if __name__ == '__main__':
	
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
	fs=fj.Feature_select()
	term_vec=fs.transform(term_str)
	x_train,x_test,y_train,y_test=train_test_split(term_vec,class_list,test_size=0.2) 
	clf = MultinomialNB().fit(x_train, y_train)  #调用MultinomialNB分类器
#	pexpected = y_test
#	ppredicted = clf.predict(x_test)
#	print(metrics.classification_report(pexpected, ppredicted))
#	print(metrics.confusion_matrix(pexpected, ppredicted))
	term_vec=fs.transform(['咖啡'])
	ppredicted = clf.predict(term_vec)
	print ppredicted[0]
