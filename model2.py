import public_fun
import pymysql

#从user_bought_history获得搭配信息


#获得模型2的值
def get_model2_value(cursor_base, cursor, item_id1, item_id2):
    if public_fun.is_two_items_same_belong(cursor, item_id1, item_id2):
        return 0
    else:
        #计算商品对(A,B)同时购买的人数
        sql = "\
            SELECT\
                COUNT(*) \
            FROM\
                ( SELECT user_id FROM user_bought_history WHERE item_id = %d ) AS tmp1\
                INNER JOIN ( SELECT user_id FROM user_bought_history WHERE item_id = %d) AS tmp2 ON tmp1.user_id = tmp2.user_id\
            " % (item_id1, item_id2)

        try:
            cursor.execute(sql)
            #搭配度是：同时购买人数*余弦相似度
            return float(cursor.fetchone()[0]) * public_fun.get_similarity(
                cursor, item_id1, item_id2)
            # return float(cursor.fetchone()[0])
        except:
            print("error model2 fail")