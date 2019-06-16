import pymysql  #导入数据库包
from sklearn.feature_extraction.text import CountVectorizer  #导入sklearn的特征提取包，计算tf
from sklearn.feature_extraction.text import TfidfTransformer  #导入sklearn的ifidf计算包，计算tf-idf
from sklearn.metrics.pairwise import cosine_similarity  #导入sklearn的计算余弦相似度的包


#获得商品所属类别ID
def get_item_belong(cursor, item_id):  #checked
    sql = "SELECT item_belong FROM dim_items WHERE item_id=%d" % int(
        item_id)  #从dim_items表中取得商品所属类别ID
    try:
        cursor.execute(sql)
        return cursor.fetchone()[0]
    except:
        print("error: get_item_belong fail")


#判断两个商品是否属于同类
def is_two_items_same_belong(cursor, item_id1, item_id2):  #checked
    item1_belong = get_item_belong(cursor, item_id1)  #获得商品1和商品2的所属类别ID
    item2_belong = get_item_belong(cursor, item_id2)
    if item1_belong == item2_belong:  #判断商品1和商品2的所属类别ID是否相同
        return True
    else:
        return False


#获得两个商品的余弦相似度（通过标题分词）
def get_similarity(cursor, item_id1, item_id2):  #checked
    sql = "SELECT\
		item_title \
	FROM\
		dim_items \
	WHERE\
		item_id = %d" % int(item_id1)  # % 是字符串格式符
    try:
        cursor.execute(sql)  #执行SQL语句
        data = cursor.fetchone()[0]  #从查询结果中把第一条记录从元组中提取出来
        # print("first item title: "+data)
        # print(data)
        data = data.replace(",", " ")  #逗号用空格分割
        two_titles = []
        two_titles.append("".join(data))  #放进去list里面
    except:
        print("error: 没有这个商品%d" % item_id1)
    # print(two_titles)

    #SQL语句：把第二个商品的信息从dim_items表中查询出来
    sql = "SELECT\
		item_title \
	FROM\
		dim_items \
	WHERE\
		item_id = %d" % int(item_id2)  # % 是字符串格式符
    try:
        cursor.execute(sql)  #执行SQL语句
        data = cursor.fetchone()[0]  #从查询结果中把第一条记录从元组中提取出来
        # print("second item title: "+data)

        data = data.replace(",", " ")  #逗号用空格分割
        two_titles.append("".join(data))  #放进去list里面
        # print(two_titles)
    except:
        print("error: 没有这个商品%d" % item_id2)
    #3.

    #将文本中的词语转换为词频矩阵
    vectorizer = CountVectorizer()
    #计算个词语出现的次数
    x = vectorizer.fit_transform(two_titles)

    #将词频矩阵X统计成TF-IDF值
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(x)
    return cosine_similarity(tfidf)[0][1]
