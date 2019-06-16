import pymysql  # 导入数据库包
import math
from sklearn.feature_extraction.text import CountVectorizer  # 导入sklearn的特征提取包，计算tf
from sklearn.feature_extraction.text import TfidfTransformer  # 导入sklearn的ifidf计算包，计算tf-idf
from sklearn.metrics.pairwise import cosine_similarity  # 导入sklearn的计算余弦相似度的包
import public_fun
#从dim_fashion_matchset获取搭配信息

global p
p = 4  #p参数
#test code
if __name__ == "__main__":
    db = pymysql.connect("localhost", "root", "password", "softwareengineering")
    cursor = db.cursor()


# 获得与商品搭配的商品数量多少
def get_item_match_count(cursor, item_id):  # checked
    sql = "SELECT item_match_count FROM item_match_count WHERE item_id=%d" % int(
        item_id)
    try:
        cursor.execute(sql)
        return cursor.fetchone()[0]
    except:
        print("error: get_item_match_count fail")


# phi值是与item_match_count正相关的函数
# 通过item_match_count计算phi值
def phi_by_count(item_match_count):  # checked
    a = 0.15
    b = 1
    # print("here? " + str(item_match_count))
    return a * math.log(int(item_match_count)) + b


# 通过item_match_id计算phi值
def phi_by_id(cursor, item_id):
    item_count = get_item_match_count(cursor, item_id)
    if item_count == 0:
        return 0
    # print(item_count)
    return phi_by_count(item_count)


# 获得model1的搭配度，及商品item1与商品item2的搭配度
def get_model1_value(cursor_base, cursor, item_id1, item_id2):

    item_belong1 = public_fun.get_item_belong(cursor, item_id1)  #item1的类别
    item_belong2 = public_fun.get_item_belong(cursor, item_id2)
    if item_belong1 == item_belong2:  #如果两个商品同类型，则不可以搭配，搭配度为0
        return 0
    else:
        value = 0  #最后结果
        phi_item2 = phi_by_id(cursor, item_id2)  #item2的phi值
        if phi_item2 == 0:
            return 0
        #test code
        if __name__ == "__main__":
            print(str(phi_item2) + " phi item2")
        sql = "SELECT item_id2,item_belong2 FROM each_item_match WHERE item_id1=%d " % int(
            item_id2)  #获得与item2搭配的商品
        try:
            cursor_base.execute(sql)
            match_items = cursor_base.fetchone()
            while match_items:
                one_match_item_id = match_items[0]  #获得搭配商品的ID
                one_match_item_belong = match_items[1]  #搭配商品类别
                if one_match_item_belong == item_belong1:  #若搭配商品与item1不是同类，则搭配度为0，否则计算item1和搭配商品的搭配度
                    similarity_one_match_item = public_fun.get_similarity(
                        cursor, item_id1, one_match_item_id)
                    phi_one_match_item = phi_by_id(cursor, one_match_item_id)
                    value += math.pow(
                        similarity_one_match_item / phi_one_match_item, p)

                match_items = cursor_base.fetchone()

            sql = "SELECT item_id1,item_belong1 FROM each_item_match WHERE item_id2=%d " % int(
                item_id2)  #获得与item2搭配的商品
            cursor_base.execute(sql)
            match_items = cursor_base.fetchone()
            while match_items:
                one_match_item_id = match_items[0]  #获得搭配商品的ID
                one_match_item_belong = match_items[1]  #搭配商品类别
                if one_match_item_belong == item_belong1:  #若搭配商品与item1不是同类，则搭配度为0，否则计算item1和搭配商品的搭配度
                    similarity_one_match_item = public_fun.get_similarity(
                        cursor, item_id1, one_match_item_id)
                    phi_one_match_item = phi_by_id(cursor, one_match_item_id)
                    value += math.pow(
                        similarity_one_match_item / phi_one_match_item, p)
                match_items = cursor_base.fetchone()
                #test code
            if __name__ == "__main__":
                print("one_match_item_id " + str(one_match_item_id))
                print("one_match_item_belong " + str(one_match_item_belong))
                print("similarity_one_match_item " +
                      str(similarity_one_match_item))
                print("phi_one_match_item" + str(phi_one_match_item))
            value = phi_item2 * math.pow(value, 1 / p)
        except:
            print("error model1 fail sql")

        return value


#test code
if __name__ == "__main__":
    print(get_model1_value(cursor, 29, 49))
    print("")
    print(get_model1_value(cursor, 2192991, 1019))

#test code
if __name__ == "__main__":
    db.close()
