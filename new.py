import pymysql #导入数据库包
from sklearn.feature_extraction.text import CountVectorizer #导入sklearn的特征提取包，计算tf
from sklearn.feature_extraction.text import TfidfTransformer #导入sklearn的ifidf计算包，计算tf-idf
from sklearn.metrics.pairwise import cosine_similarity #导入sklearn的计算余弦相似度的包

#1.
item_id1=int(input("first item id: ")) #输入两个商品的ID
item_id2=int(input("second item id: "))
# item_id1=29
# item_id2=49

#2.
db=pymysql.connect("localhost","root","474102","softwareengineering") #连接数据库
cursor=db.cursor() #创建操作游标
#SQL语句：把第一个商品的信息从dim_items表中查询出来
sql="SELECT\
	item_title \
FROM\
	dim_items \
WHERE\
	item_id = %d" %item_id1 # % 是字符串格式符
try:
	cursor.execute(sql)#执行SQL语句
	data=cursor.fetchone()[0]#从查询结果中把第一条记录从元组中提取出来
	print("first item title: "+data)
	# print(data)
	data=data.replace(","," ")#逗号用空格分割
	two_titles=[]
	two_titles.append("".join(data))  #放进去list里面
except:
	print("error: 没有这个商品%d"%item_id1)
# print(two_titles)

#SQL语句：把第二个商品的信息从dim_items表中查询出来
sql="SELECT\
	item_title \
FROM\
	dim_items \
WHERE\
	item_id = %d" %item_id2 # % 是字符串格式符
try:
	cursor.execute(sql)#执行SQL语句
	data=cursor.fetchone()[0]#从查询结果中把第一条记录从元组中提取出来
	print("second item title: "+data)

	db.close() #关闭数据库连接

	data=data.replace(","," ")#逗号用空格分割
	two_titles.append("".join(data)) #放进去list里面
	# print(two_titles)
except:
	print("error: 没有这个商品%d"%item_id2)
#3.

#将文本中的词语转换为词频矩阵
vectorizer=CountVectorizer()
#计算个词语出现的次数
x=vectorizer.fit_transform(two_titles)

#将词频矩阵X统计成TF-IDF值
transformer=TfidfTransformer()
tfidf=transformer.fit_transform(x)

#利用TF-IDF值计算余弦相似度
distance=cosine_similarity(tfidf)
print("\ncosine similarity between two items: ",distance[0][1])