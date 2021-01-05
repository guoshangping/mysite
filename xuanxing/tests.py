# -*- coding:utf-8 -*-
import json
import os
import json

dict = {}


# 用来存储数据

def get_json_data():
    # 获取json里面数据
    params = {}
    with open('fxn1.json', 'rb') as f:
        # 定义为只读模型，并定义名称为f
        params = json.load(f)
        params["a"].append("dasda")
        # 加载json文件中的内容给params
        print("params", params)
        # 将修改后的内容保存在dict中
    with open('./fxn1.json', 'w') as r:
        # 定义为写模式，名称定义为r
        json.dump(params, r)


def write_json_data(dict):
    # 写入json文件

    with open('out', 'w') as r:
        # 定义为写模式，名称定义为r

        json.dump(dict, r)
        # 将dict写入名称为r的文件中

    r.close()
    # 关闭json写模式


if __name__ == '__main__':
    get_json_data()
