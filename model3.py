import public_fun

#只从dim_items获得搭配信息


#model3的值
def get_model3_value(cursor_base, cursor, item_id1, item_id2):
    if public_fun.is_two_items_same_belong(cursor, item_id1, item_id2):
        return 0  #如果两个商品是同类，则搭配值为0
    else:
        return public_fun.get_similarity(cursor, item_id1,
                                         item_id2)  #如果两个商品不同类，则返回它们的余弦相似度作为搭配度
