import model1
import model2
import model3
import public_fun
import sys
import pymysql
import time
from random import randint

global not_exceed_10  #全局变量，用来判断列表是否超过10个元素
not_exceed_10 = True

time_start = time.time()  #计开始时
#连接数据库，输入数据库名，密码，表名
db2 = pymysql.connect("localhost", "root", "474102", "softwareengineering")
cursor = db2.cursor()  #数据库游标。用来进行各种混杂的查询
db3 = pymysql.connect("localhost",
                      "root",
                      "474102",
                      "softwareengineering",
                      cursorclass=pymysql.cursors.SSCursor)
cursor_base2 = db3.cursor()  #sscursor数据库游标，专门用来读取大量数据用
p1 = 1  #model1的权重
# p2 = 0.5 #model2的权重
p3 = 0.3  #model3的权重
item_id1 = input("input item_id1: ")  #输入一个商品A的ID
item_belong1 = public_fun.get_item_belong(cursor, item_id1)  #得到这个商品的类别ID

final_match_item_ids = []  #list存储最后搭配的商品ID
final_match_item_values = []  #list存储最后搭配的商品的搭配度

candidate_items_num = 500  #尝试搭配的次数

sql = "SELECT MAX(item_id) FROM dim_items"  #获取商品最大ID
cursor.execute(sql)
max_item_id = cursor.fetchone()[0]

min_value = sys.float_info.max  #临时变量，用来存储final_match_item_values中的
while candidate_items_num > 0:  #尝试搭配candidate_item_num次
    candidate_items_num -= 1
    match_item_id = randint(1, max_item_id)  #随机选取一个可能搭配的商品B
    sql = "SELECT item_belong FROM dim_items WHERE item_id=%d" % int(
        match_item_id)
    cursor.execute(sql)
    match_item_belong = cursor.fetchone()
    if match_item_belong:
        match_item_belong = match_item_belong[0]  #获取商品B的类别ID
        if match_item_belong == item_belong1:  #如果商品B和商品A属于同类，则搭配失败，尝试下一次
            candidate_items_num += 1
        else:
            #获得model1,2,3的值
            model1_value = model1.get_model1_value(cursor_base2, cursor, 29,
                                                   match_item_id)
            model2_value = model2.get_model2_value(cursor_base2, cursor, 29,
                                                   match_item_id)
            model3_value = model3.get_model3_value(cursor_base2, cursor, 29,
                                                   match_item_id)
            #根据model1,2,3获得最终商品A，B的搭配度
            match_value = p1 * model1_value + model2_value + p3 * model3_value
            length_list = len(
                final_match_item_ids)  #获得final_match_item_ids的元素数量
            if length_list < 10:
                #final_match_item_ids里面不足10个商品，直接放入商品B即可
                final_match_item_ids.append(int(match_item_id))
                final_match_item_values.append(float(match_value))
                # print("test: " + str(final_match_item_ids))
                # print("test" + str(final_match_item_values))
                # print("match_value " + str(match_value) + " = model1_value " +
                #       str(model1_value) + " +model2_value " +
                #       str(model2_value) + " +model3_value " +
                #       str(model3_value))
            else:
                if not_exceed_10:
                    not_exceed_10 = False
                    min_value = float(
                        min(final_match_item_values)
                    )  #只有当每次更新final_match_item_ids的时候才求取一次minimum，减少计算次数
                if min_value < match_value:
                    #如果当前商品B的搭配度比final_match_item_ids中的某个商品大，则可以把这个商品B替换进去
                    min_value_index = final_match_item_values.index(
                        min_value)  #获取minimum的下标
                    final_match_item_ids[min_value_index] = int(
                        match_item_id)  #加入商品B
                    final_match_item_values[min_value_index] = float(
                        match_value)  #加入商品B的搭配
                    min_value = float(
                        min(final_match_item_values)
                    )  #只有当每次更新final_match_item_ids的时候才求取一次minimum，减少计算次数
                    # print("test: " + str(final_match_item_ids))
                    # print("test" + str(final_match_item_values))
                    # print("match_value " + str(match_value) +
                    #       " = model1_value " + str(model1_value) +
                    #       " +model2_value " + str(model2_value) +
                    #       " +model3_value " + str(model3_value))
    else:
        candidate_items_num += 1

# final_match_item_ids.sort(reverse=True)#把搭配商品列表根据搭配度排序
# final_match_item_values.sort(reverse=True)
print(final_match_item_ids)  #把搭配商品列表打印出来
print(final_match_item_values)  #把搭配商品的搭配度列表打印出来

time_end = time.time()
print("cost time: ", time_end - time_start)

#关闭数据库连接
db2.close()
db3.close()